from django.urls import path
# from .views import (ExamDetailView,ExamDetailListView,ExamDetailDeleteView,
#                     ExamDetailUpdateView,ExamSlotView,ExamSlotListView,
#                     ExamSlotUpdateView,ExamSlotDeleteView,PaperTypeView,
#                     PaperTypeListView,PaperTypeUpdateView,PaperTypeDeleteView,
#                     ExamModeView,ExamModeListView,ExamModeUpdateView,
#                     ExamModeDeleteView,RegionView,RegionListView,
#                     RegionUpdateView,RegionDeleteView,StateView,
#                     StateListView,StateUpdateView,StateDeleteView,
#                     ExamCodeListView,RegionDropdownView,StateDropdownView,
#                     CityDropdownView,CityView,CityUpdateView,CityDeleteView,
#                     CityListView,CenterView,CenterListView)


from . views import *

urlpatterns = [
    # Dropdown API's
    path('examcode-list', ExamCodeListView.as_view(), name='examcode-list'), # examcode-downlist,
    path('exammode-list', ExamModeDropdownView.as_view(), name='exammode-list'), # exammode-downlist
    path('region-dropdown-list', RegionDropdownView.as_view(), name='region-dropdown-list'),# region-dropdown
    path('state-dropdown-list', StateDropdownView.as_view(), name='state-dropdown-list'), # state-dropdown
    path('city-dropdown-list', CityDropdownView.as_view(), name='city-dropdown-list'), # city-dropdown
    path('rating-dropdown-list', RatingDropdownView.as_view(), name='rating-dropdown-list'), # rating-dropdown
    path('centerstatus-dropdown-list', CenterStatusDropdownView.as_view(), name='centerstatus-dropdown-list'), # status-dropdown
    path('membertype-dropdown-list', MemberTypeDropdownView.as_view(), name='membertype-dropdown-list'), # status-dropdown
    path('memberrole-dropdown-list', ExamMemberRoleDropdownView.as_view(), name='memberrole-dropdown-list'), # role-dropdown

    
    # Exam Details URL'S
    path('exam-details',ExamDetailView.as_view(), name='exam-details'),
    path('exam-details-list',ExamDetailListView.as_view(),name='exam-detail-list'),
    path('exam-details-update', ExamDetailUpdateView.as_view(), name='exam-detail-update'),
    path('exam-details-delete', ExamDetailDeleteView.as_view(), name='exam-detail-delete'),
    # Exam Slot URL'S
    path('exam-slot',ExamSlotView.as_view(),name='exam-slot'),
    path('exam-slot-list',ExamSlotListView.as_view(),name='exam-slot-list'),
    path('exam-slot-update', ExamSlotUpdateView.as_view(), name='exam-slot-update'),
    path('exam-slot-delete', ExamSlotDeleteView.as_view(), name='exam-slot-delete'),
    # Exam Papertype URL'S
    path('exam-papertype',PaperTypeView.as_view(),name='exam-papertype'),
    path('exam-papertype-list',PaperTypeListView.as_view(),name='exam-papertype-list'),
    path('exam-papertype-update', PaperTypeUpdateView.as_view(), name='exam-papertype-update'),
    path('exam-papertype-delete', PaperTypeDeleteView.as_view(), name='exam-papertype-delete'),
    # Exam Mode URL'S
    path('exam-mode',ExamModeView.as_view(),name='exam-mode'),
    path('exam-mode-list',ExamModeListView.as_view(),name='exam-mode-list'),
    path('exam-mode-update', ExamModeUpdateView.as_view(), name='exam-mode-update'),
    path('exam-mode-delete', ExamModeDeleteView.as_view(), name='exam-mode-delete'),
    # Region API's
    path('region-view',RegionView.as_view(),name='region-view'),
    path('region-view-list',RegionListView.as_view(),name='region-view-list'),
    path('region-view-update', RegionUpdateView.as_view(), name='region-view-update'),
    path('region-view-delete', RegionDeleteView.as_view(), name='region-view-delete'),
    # State API's
    path('state-view',StateView.as_view(),name='state-view'),
    path('state-view-list',StateListView.as_view(),name='state-view-list'),
    path('state-view-update', StateUpdateView.as_view(), name='state-view-update'),
    path('state-view-delete', StateDeleteView.as_view(), name='state-view-delete'),
    # City API's
    path('city-view',CityView.as_view(),name='city-view'),
    path('city-view-list',CityListView.as_view(),name='city-view-list'),
    path('city-view-update', CityUpdateView.as_view(), name='city-view-update'),
    path('city-view-delete', CityDeleteView.as_view(), name='city-view-delete'),
    #Center View API's
    path('center-view',CenterView.as_view(),name='center-view'),
    path('center-view-list',CenterListView.as_view(),name='center-view-list'),
    path('center-view-update',CenterUpdateView.as_view(),name='center-view-update'),
    path('center-view-delete',CenterDeleteView.as_view(),name='center-view-delete'),
    # ExamDevice API URLs
    path('exam-device', ExamDeviceView.as_view(), name='exam-device'),               
    path('exam-device-list', ExamDeviceListView.as_view(), name='exam-device-list'), 
    path('exam-device-update', ExamDeviceUpdateView.as_view(), name='exam-device-update'), 
    path('exam-device-delete', ExamDeviceDeleteView.as_view(), name='exam-device-delete'),
    # ExamRole API URL Patterns
    path('exam-role', ExamRoleView.as_view(), name='exam-role'),
    path('exam-role-list', ExamRoleListView.as_view(), name='exam-role-list'),
    path('exam-role-update', ExamRoleUpdateView.as_view(), name='exam-role-update'),
    path('exam-role-delete', ExamRoleDeleteView.as_view(), name='exam-role-delete'),
    # ExamRole API URL Patterns
    path('exam-member', ExamMemberView.as_view(), name='exam-member'),
    path('exam-member-list', ExamMemberListView.as_view(), name='exam-member-list'),
    path('exam-member-update', ExamMemberUpdateView.as_view(), name='exam-member-update'),
    path('exam-member-delete', ExamMemberDeleteView.as_view(), name='exam-member-delete'),

    


]