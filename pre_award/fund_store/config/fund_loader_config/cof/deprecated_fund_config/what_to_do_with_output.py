# flake8: noqa
# The following lists are samples of the extracted  data from the current section display config
# for both application and assessment
# Use the functions in the following files to get the data required for database input:
# 1. sort_application_sections.py
# 2. sort_assessment_sections.py
# ^ These functions are only necessary to transform existing config
# A sample data output of functions 1 and 2 is below
# It is envisaged that this data format below (and the steps outlined) will be the required input config for future rounds
### APPLICATION ###
# an_sorted_application_sections_SAMPLE = [
#     {'section_name': 'About your organisation', 'tree_path': '1'},
#     {'section_name': 'Organisation Information', 'tree_path': '1.1'},
#     {'section_name': 'Applicant Information', 'tree_path': '1.2'},
#     {'section_name': 'About your project', 'tree_path': '2'},
#     {'section_name': 'Project Information', 'tree_path': '2.1'},
#     {'section_name': 'Asset Information', 'tree_path': '2.2'},
#     {'section_name': 'Strategic case', 'tree_path': '3'},
#     {'section_name': 'Community Use', 'tree_path': '3.1'},
#     {'section_name': 'Community Engagement', 'tree_path': '3.2'},
#     {'section_name': 'Local Support', 'tree_path': '3.3'},
#     {'section_name': 'Environmental Sustainability', 'tree_path': '3.4'},
#     {'section_name': 'Management case', 'tree_path': '4'},
#     {'section_name': 'Funding Required', 'tree_path': '4.1'},
#     {'section_name': 'Feasibility', 'tree_path': '4.2'}
#     # ...etc
# ]
# ### SQL
# # 3. Insert into SECTIONS_TABLE
# # for section in an_sorted_sections :
# #     INSERT INTO SECTIONS_TABLE(path_value, section_names, service)
# #       values (section["tree_path"], section["section_name"], assessmentORapplication);
# ### ASSESSMENT ###
# # The assessment script outputs three items for database insert (they are explained in the scripts further down this page)
# # {
# #   "sorted_scored_sections": [...],
# #   "sorted_unscored_sections": [...],
# #   "all_fields": [...]
# # }
# all_an_sorted_sections_scored_SAMPLE = [
#     {'section_name': 'strategic_case', 'tree_path': '1.1', 'weighting': 0.3},
#     {'section_name': 'benefits', 'tree_path': '1.1.1', 'weighting': None},
#     {'section_name': 'community_use', 'tree_path': '1.1.1.1', 'weighting': None, 'fields': [
#         {'id': 'WWWWxy', 'display_order': 10},
#         {'id': 'YdtlQZ', 'display_order': 20},
#         {'id': 'iBCGxY', 'display_order': 30},
#         {'id': 'PHFkCs', 'display_order': 10},
#         {'id': 'QgNhXX', 'display_order': 20},
#         {'id': 'XCcqae', 'display_order': 30},
#         {'id': 'lajFtB', 'display_order': 10},
#         {'id': 'plmwJv', 'display_order': 20},
#         {'id': 'GlPmCX', 'display_order': 60},
#         {'id': 'GvPSna', 'display_order': 10},
#         {'id': 'zsbmRx', 'display_order': 20},
#         {'id': 'aHIGbK', 'display_order': 80},
#         {'id': 'DwfHtk', 'display_order': 90},
#         {'id': 'MPNlZx', 'display_order': 100},
#      ...
#      ]},
#     {'section_name': 'risk_loss_impact', 'tree_path': '1.1.1.2',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'engagement', 'tree_path': '1.1.2', 'weighting': None},
#     {'section_name': 'engaging-the-community',
#         'tree_path': '1.1.2.1', 'weighting': None, 'fields': [...]},
#     {'section_name': 'local-support', 'tree_path': '1.1.2.2',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'environmental_sustainability',
#         'tree_path': '1.1.3', 'weighting': None},
#     {'section_name': 'environmental-considerations',
#         'tree_path': '1.1.3.1', 'weighting': None, 'fields': [...]},
#     {'section_name': 'management_case', 'tree_path': '1.2', 'weighting': 0.3},
#     {'section_name': 'funding_breakdown', 'tree_path': '1.2.1', 'weighting': None},
#     {'section_name': 'funding_requested', 'tree_path': '1.2.1.1',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'financial_and_risk_forecasts',
#         'tree_path': '1.2.2', 'weighting': None},
#     {'section_name': 'feasibility', 'tree_path': '1.2.2.1',
#         'weighting': None, 'fields': [...]},
#     ...]
# all_an_sorted_sections_unscored_SAMPLE = [
#     {'section_name': 'unscored', 'tree_path': '2.1', 'weighting': None},
#     {'section_name': 'org_info', 'tree_path': '2.1.1', 'weighting': None},
#     {'section_name': 'general_info', 'tree_path': '2.1.1.1',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'activities', 'tree_path': '2.1.1.2',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'partnerships', 'tree_path': '2.1.1.3',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'applicant_info', 'tree_path': '2.1.2', 'weighting': None},
#     {'section_name': 'contact_information', 'tree_path': '2.1.2.1',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'project_info', 'tree_path': '2.1.3', 'weighting': None},
#     {'section_name': 'previous_funding', 'tree_path': '2.1.3.1',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'project_summary', 'tree_path': '2.1.3.2',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'asset_info', 'tree_path': '2.1.4', 'weighting': None},
#     {'section_name': 'asset_ownership', 'tree_path': '2.1.4.1',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'asset_evidence', 'tree_path': '2.1.4.2',
#         'weighting': None, 'fields': [...]},
#     {'section_name': 'asset_background', 'tree_path': '2.1.4.3',
#         'weighting': None, 'fields': [...]},
#     ...]
# all_fields_SAMPLE = [
#     {
#         'form_json_id': 'kxgWTy',
#         'type': 'multilineTextField',
#         'presentation_type': 'text',
#         'title': 'Who in the community uses the asset, or has used it in the past, and who benefits from it?'
#     },
#     {
#         'form_json_id': 'wudRxx',
#         'type': 'multilineTextField',
#         'presentation_type': 'text',
#         'title': "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community"
#     }
#     ...]
### SQL
# INSERT ALL NEW FIELDS
# for field in all_fields:
# INSERT INTO ASSESSMENT_FIELDS(form_json_id,type,presentation_type,title)
#   VALUES(field["form_json_id"],field["type"],field["presentation_type"],field["title"], )
# reject conflicts
# Funds will be reusing forms so we only need to load new fields
# INSERT SECTIONS
# for section in all_an_sorted_sections_unscored:
#     INSERT INTO SECTIONS_TABLE(path_value, section_name, weighting, assessmentORapplication)
#       values (etc);
# If this is the lowest level section it will have a "fields" key.
#   if "fields" in section:
#       for field in fields:
#           INSERT INTO SECTIONS_FIELDS(field_id, section_id, display_order)
#           values (etc);
#           ^ get the section_id from section INSERT above
# NOTE
# There are some instances of duplicate field_ids in the assessment mapping (a single field_id to many assessment field mapping objects),
# suspected because we need to break an application field into multiple assessment elements.
# We should aim to have a 1-1 mapping of fields from application to assessment
# We could handle this locally in the assessment frontend for that type and presentation_type,
# rather than complicate our data model. This may only be true for "add-another" fields (need further investigation).
# This needs further discussion and as it stands, in some cases we store many fields_ids in our mapping
# for one application component
# Changes to remove this behavior on add-another fields to be implemented as part of fs-2500
# the same is found in reverse (many field_ids to one assessment field mapping object),
# many field ids map (are grouped) to one assessment componenet as a list of field_ids
# suspected because we need to consume multiple fields into one assessment field view.
# At the moment this is handled by giving these grouped ids the same display_order (i.e: all 10)
