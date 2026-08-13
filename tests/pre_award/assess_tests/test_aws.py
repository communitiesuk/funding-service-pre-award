import pre_award.assess
from pre_award.assess.services.aws import FileData, generate_url, list_files_in_folder


def test_generate_url_short_id(app):
    file_data = FileData("app1", "form1", "path1", "comp1", "file1.txt")
    assert (
        generate_url(file_data, "short-id")
        == "http://assessment.communities.gov.localhost:3010/assess/application/app1/export/form1%252Fpath1%252Fcomp1%252Ffile1.txt?short_id=short-id&quoted=True"
    )


def test_generate_url(app):
    file_data = FileData("app1", "form1", "path1", "comp1", "file1.txt")
    assert (
        generate_url(file_data)
        == "http://assessment.communities.gov.localhost:3010/assess/application/app1/export/form1%252Fpath1%252Fcomp1%252Ffile1.txt?quoted=True"
    )


def test_list_files_in_folder(monkeypatch):
    def mock_list_objects_v2(Bucket, Prefix):  # noqa
        return {
            "Contents": [
                {"Key": "app_id/form_name/path/name/filename1.png"},
                {"Key": "app_id/form_name/path/name/filename2.docx"},
                {"Key": "app_id/form_name/path/name/filename3.jpeg"},
                {"Key": "app_id/form_name/path/name/filename4.png"},
                {"Key": "app_id/form_name/path/name/filename5.pdf"},
                {"Key": "app_id/form_name/path/name/filename6.txt"},
                {"Key": "app_id/form_name/path/name/filename7.doc"},
                {"Key": "app_id/form_name/path/name/filename8.docx"},
                {"Key": "app_id/form_name/path/name/filename9.odt"},
                {"Key": "app_id/form_name/path/name/filename10.csv"},
                {"Key": "app_id/form_name/path/name/filename11.xls"},
                {"Key": "app_id/form_name/path/name/filename12.xlsx"},
                {"Key": "app_id/form_name/path/name/filename13.ods"},
            ]
        }

    monkeypatch.setattr(
        pre_award.assess.services.aws._S3_CLIENT,
        "list_objects_v2",
        mock_list_objects_v2,
    )

    prefix = "app_id/form_name/path/name/"
    files = list_files_in_folder(prefix)

    assert files == [
        "form_name/path/name/filename1.png",
        "form_name/path/name/filename2.docx",
        "form_name/path/name/filename3.jpeg",
        "form_name/path/name/filename4.png",
        "form_name/path/name/filename5.pdf",
        "form_name/path/name/filename6.txt",
        "form_name/path/name/filename7.doc",
        "form_name/path/name/filename8.docx",
        "form_name/path/name/filename9.odt",
        "form_name/path/name/filename10.csv",
        "form_name/path/name/filename11.xls",
        "form_name/path/name/filename12.xlsx",
        "form_name/path/name/filename13.ods",
    ]


def test_list_files_in_folder_pages_through_truncated_results(monkeypatch):
    """list_objects_v2 caps at 1000 keys per call; list_files_in_folder must page through
    ContinuationToken/IsTruncated until exhausted rather than silently dropping the rest."""
    calls = []

    def mock_list_objects_v2(**kwargs):
        calls.append(kwargs)
        if kwargs.get("ContinuationToken") is None:
            return {
                "Contents": [{"Key": "app_id/file1.png"}],
                "IsTruncated": True,
                "NextContinuationToken": "token-1",
            }
        assert kwargs["ContinuationToken"] == "token-1"
        return {
            "Contents": [{"Key": "app_id/file2.png"}],
            "IsTruncated": False,
        }

    monkeypatch.setattr(
        pre_award.assess.services.aws._S3_CLIENT,
        "list_objects_v2",
        mock_list_objects_v2,
    )

    files = list_files_in_folder("app_id/")

    assert files == ["file1.png", "file2.png"]
    assert len(calls) == 2
