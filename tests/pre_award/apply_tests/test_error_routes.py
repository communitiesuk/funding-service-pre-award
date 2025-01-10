from bs4 import BeautifulSoup

from pre_award.config import Config


def test_404(apply_test_client):
    response = apply_test_client.get("not_found")

    assert response.status_code == 404
    soup = BeautifulSoup(response.data, "html.parser")
    assert len(soup.find_all("a", href=Config.SUPPORT_DESK_APPLY)) == 1
