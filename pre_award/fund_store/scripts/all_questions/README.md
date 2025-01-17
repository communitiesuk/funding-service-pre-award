# All Questions Generation
The scripts in this folder are used to generate the 'all questions' page for a fund. They take the section information from the fund-store database, combine it with the question flow from the form jsons, to generate a single HTML page containing all questions and all possible branches for a particular round.

Instructions on running the script and what to do with the outputs are in confluence: https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/45580513/Generating+the+All+Questions+page+and+Assessment+Field+Display+info


## Generating test data
This is for testing [build_hierarchy_levels_for_page](./metadata_utils.py), or anything that takes in the full form json. You can use the full form json, or if you want to use a subset of the form json to make debugging easier, these instructions allow you to extract a small portion of the form for easier testing.

These steps are to help with debugging by separating out the steps or just extracting a subset of the form.

In order to make debugging easier, there are methods to extract a subset of data from a form, to test a particular combination of questions and conditions. You can also save the 'metadata' used for the hierarchy information to a file to again make debugging easier.

### To generate meta data
1. Un-skip the test `test_generate_metadata` in [test_generate_all_questions.py](../../tests/test_generate_all_questions.py)
1. Update the `path_to_form` to the form you want metadata for
1. Execute this single test

### To generate test data
If you are testing against metadata for the whole form, you don't need this bit, just the meta data. This allows you to generate metadata for a subset of a form, basically setting the start and end pages to somewhere in the middle of the form.
1. Generate metadata, as per above instructions
1. Look at the dict objects defined in [generate_test_data.py](./generate_test_data.py) - these are how you define the subset of the form you want to test. Update the start and end paths for the subset you want, and include every path you want in between the in the `pages` list.
1. Unskip `test_generate_test_data` in [test_generate_all_questions.py](../../tests/test_generate_all_questions.py)
1. Update the out path and input path (uses the metadata_path from above by default)
1. Update the `files_to_generate` path to use the dict you defined above.
1. Execute this single test

### Testing build_hierarchy_levels_for_page
You can now write a test using `build_hierarchy_levels_for_page` with either a whole form of metadata, or just a subset. Use the output paths above as input to your test.
