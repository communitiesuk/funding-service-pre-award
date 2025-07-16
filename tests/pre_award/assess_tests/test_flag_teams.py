from pre_award.assess.assessments.models.flag_teams import TeamsFlagData
from pre_award.assess.services.models.flag import Flag


class TestTeamsFlagData:
    @staticmethod
    def create_flag(
        id,
        sections_to_flag,
        latest_status,
        latest_allocation,
        application_id,
        updates,
    ):
        return Flag(
            id=id,
            sections_to_flag=sections_to_flag,
            latest_status=latest_status,
            latest_allocation=latest_allocation,
            application_id=application_id,
            updates=updates,
            field_ids=[],
            is_change_request=False,
        )

    def test_from_flags_with_empty_list(self):
        teams_data = TeamsFlagData.from_flags([])
        assert teams_data.teams_stats == {}

    def test_from_flags_with_single_flag(self):
        flag = self.create_flag("1", ["section1", "section2"], "RAISED", "TeamA", "AppA", [])
        teams_data = TeamsFlagData.from_flags([flag])
        assert len(teams_data.teams_stats) == 1
        assert teams_data.teams_stats["TeamA"].num_of_flags == 1
        assert teams_data.teams_stats["TeamA"].num_of_raised == 1
        assert teams_data.teams_stats["TeamA"].num_of_resolved == 0
        assert teams_data.teams_stats["TeamA"].num_of_stopped == 0

    def test_from_flags_with_multiple_flags(self):
        flags = [
            self.create_flag("1", ["section1", "section2"], "RAISED", "TeamA", "AppA", []),
            self.create_flag("2", ["section3"], "RESOLVED", "TeamB", "AppB", []),
            self.create_flag("3", ["section4", "section5"], "STOPPED", "TeamA", "AppC", []),
            self.create_flag("4", ["section6"], "RAISED", "TeamA", "AppD", []),
        ]

        teams_data = TeamsFlagData.from_flags(flags)
        assert len(teams_data.teams_stats) == 2
        assert teams_data.teams_stats["TeamA"].num_of_flags == 3
        assert teams_data.teams_stats["TeamA"].num_of_raised == 2
        assert teams_data.teams_stats["TeamA"].num_of_resolved == 0
        assert teams_data.teams_stats["TeamA"].num_of_stopped == 1

        # Check if the ordinals render correctly for the RAISED flags
        assert teams_data.teams_stats["TeamA"].ordinal_list == [
            "Third",
            "Second",
            "First",
        ]

        assert teams_data.teams_stats["TeamB"].num_of_flags == 1
        assert teams_data.teams_stats["TeamB"].num_of_raised == 0
        assert teams_data.teams_stats["TeamB"].num_of_resolved == 1
        assert teams_data.teams_stats["TeamB"].num_of_stopped == 0
        assert teams_data.teams_stats["TeamB"].ordinal_list == [
            "First",
        ]

    def test_from_flags_with_no_team_allocation(self):
        """Test flags with None allocation (no teams setup)"""
        flags = [
            self.create_flag("1", ["section1"], "RAISED", None, "AppA", []),
            self.create_flag("2", ["section2"], "RESOLVED", None, "AppB", []),
        ]

        teams_data = TeamsFlagData.from_flags(flags)
        assert len(teams_data.teams_stats) == 1
        assert None in teams_data.teams_stats
        assert teams_data.teams_stats[None].team_name is None
        assert teams_data.teams_stats[None].num_of_flags == 2
        assert teams_data.teams_stats[None].num_of_raised == 1
        assert teams_data.teams_stats[None].num_of_resolved == 1

    def test_from_flags_mixed_allocation_and_none(self):
        """Test flags with both team allocation and None allocation"""
        flags = [
            self.create_flag("1", ["section1"], "RAISED", "TeamA", "AppA", []),
            self.create_flag("2", ["section2"], "RAISED", None, "AppB", []),
            self.create_flag("3", ["section3"], "RESOLVED", "TeamA", "AppC", []),
            self.create_flag("4", ["section4"], "STOPPED", None, "AppD", []),
        ]

        teams_data = TeamsFlagData.from_flags(flags)
        assert len(teams_data.teams_stats) == 2

        # Check TeamA stats
        assert teams_data.teams_stats["TeamA"].num_of_flags == 2
        assert teams_data.teams_stats["TeamA"].num_of_raised == 1
        assert teams_data.teams_stats["TeamA"].num_of_resolved == 1

        # Check None allocation stats
        assert teams_data.teams_stats[None].team_name is None
        assert teams_data.teams_stats[None].num_of_flags == 2
        assert teams_data.teams_stats[None].num_of_raised == 1
        assert teams_data.teams_stats[None].num_of_stopped == 1

    def test_from_flags_only_none_allocations(self):
        """Test when all flags have None allocation (no teams configured)"""
        flags = [
            self.create_flag("1", ["section1"], "RAISED", None, "AppA", []),
            self.create_flag("2", ["section2"], "RAISED", None, "AppB", []),
            self.create_flag("3", ["section3"], "RESOLVED", None, "AppC", []),
        ]

        teams_data = TeamsFlagData.from_flags(flags)
        assert len(teams_data.teams_stats) == 1
        assert None in teams_data.teams_stats

        none_stats = teams_data.teams_stats[None]
        assert none_stats.team_name is None
        assert none_stats.num_of_flags == 3
        assert none_stats.num_of_raised == 2
        assert none_stats.num_of_resolved == 1
        assert none_stats.num_of_stopped == 0
        assert none_stats.ordinal_list == ["Third", "Second", "First"]
