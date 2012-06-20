from urllib import unquote

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import QueryDict

from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer

from remo.profiles.helpers import get_avatar_url
from remo.profiles.models import UserProfile, FunctionalArea


class FunctionalAreasResource(ModelResource):
    """Functional Areas Resource."""

    class Meta:
        queryset = FunctionalArea.objects.all()
        resource_name = 'functionalareas'
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        include_resource_uri = False
        include_absolute_url = False
        allowed_methods = ['get']
        fields = ['name']
        filtering = {'name': ALL}


class ProfileResource(ModelResource):
    """Profile Resource."""
    profile_url = fields.CharField()
    avatar_url = fields.CharField()
    mentor = fields.BooleanField()
    council = fields.BooleanField()
    functional_areas = fields.ToManyField(FunctionalAreasResource,
                                          attribute='functional_areas',
                                          full=True, null=True)

    class Meta:
        queryset = UserProfile.objects.filter(registration_complete=True)
        resource_name = 'profile'
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        include_resource_uri = False
        include_absolute_url = False
        allowed_methods = ['get']
        fields = ['city', 'region', 'country', 'display_name', 'local_name',
                  'lon', 'lat', 'mozillians_profile_url', 'twitter_account',
                  'facebook_url', 'diaspora_url', 'personal_blog_feed',
                  'irc_name']
        ordering = ['country']
        filtering = {'display_name': ALL,
                     'local_name': ALL,
                     'irc_name': ALL,
                     'country': ALL,
                     'region': ALL,
                     'city': ALL,
                     'functional_areas': ALL_WITH_RELATIONS}

    def dehydrate_profile_url(self, bundle):
        """Calculate and return full url to Rep profile."""
        return (settings.SITE_URL + reverse('profiles_view_profile',
                                            kwargs={'display_name':
                                                    bundle.obj.display_name}))

    def dehydrate_avatar_url(self, bundle):
        """Calculate and return full avatar of Rep."""
        return get_avatar_url(bundle.obj.user, -1)

    def dehydrate_mentor(self, bundle):
        """Calculate and return full avatar of Rep."""
        return bundle.obj.user.groups.filter(name='Mentor').count() == 1

    def dehydrate_council(self, bundle):
        """Calculate and return full avatar of Rep."""
        return bundle.obj.user.groups.filter(name='Council').count() == 1


class RepResource(ModelResource):
    """Rep Resource."""
    fullname = fields.CharField(attribute='get_full_name')
    profile = fields.ToOneField(ProfileResource, attribute='userprofile',
                                full=True, null=True)

    class Meta:
        queryset = User.objects.filter(userprofile__registration_complete=True,
                                       groups__name='Rep')
        resource_name = 'rep'
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        serializer = Serializer(formats=['json', 'jsonp'])
        allowed_methods = ['get']
        fields = ['email', 'first_name', 'last_name']
        ordering = ['profile', 'first_name', 'last_name']
        filtering = {'first_name': ALL,
                     'last_name': ALL,
                     'profile': ALL_WITH_RELATIONS}

    def apply_filters(self, request, applicable_filters):
        """Add special 'query' parameter to filter Reps.

        When 'query' parameter is present, Rep list is filtered by last
        name, first name, display name and local name with a case
        insensitive matching method.

        The 'query' parameters exists in parallel with 'filter'
        parameters as defined by tastypie and RepResource schema.
        """

        base_object_list = (super(RepResource, self).
                            apply_filters(request, applicable_filters))

        query = request.GET.get('query', None)
        if query:
            query = unquote(query)
            # We need to split query to match full names
            qset = Q()
            for term in query.split():
                for key in ('first_name__istartswith',
                            'last_name__istartswith'):
                    qset |= Q(**{key: term})
            qset |= (Q(userprofile__display_name__istartswith=query)|
                     Q(userprofile__local_name__istartswith=query)|
                     Q(userprofile__irc_name__istartswith=query)|
                     Q(email__istartswith=query)|
                     Q(userprofile__private_email__istartswith=query))

            base_object_list = base_object_list.filter(qset).distinct()

        group = request.GET.get('group', None)
        if group:
            if group == 'mentor':
                base_object_list = (base_object_list.
                                    filter(groups__name='Mentor'))
            elif group == 'council':
                base_object_list = (base_object_list.
                                    filter(groups__name='Council'))
            elif group == 'rep':
                base_object_list = (base_object_list.
                                    filter(groups__name='Rep'))

        return base_object_list

    def apply_sorting(self, obj_list, options=None):
        """Add support for multiple order_by parameters."""
        if ',' in options.get('order_by', ''):
            order_by_values = []
            for param in options['order_by'].split(','):
                q = QueryDict('order_by=%s' % param)
                obj_list = super(RepResource, self).apply_sorting(obj_list, q)
                order_by_values.append(obj_list.query.order_by[0])

            return obj_list.order_by(*order_by_values)

        return super(RepResource, self).apply_sorting(obj_list, options)