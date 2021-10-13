import pytest

from hier_config.host import Host


class TestHost:
    @pytest.fixture(autouse=True)
    def setup(self, options_ios):
        self.host = Host("example.rtr", "ios", options_ios)
        self.host_bltn_opts = Host("example.rtr", "ios")

    def test_load_config_from(self, running_config, generated_config):
        self.host.load_running_config(running_config)
        self.host.load_generated_config(generated_config)
        self.host_bltn_opts.load_running_config(running_config)
        self.host_bltn_opts.load_generated_config(generated_config)

        assert len(self.host.generated_config) > 0
        assert len(self.host.running_config) > 0
        assert len(self.host_bltn_opts.running_config) > 0
        assert len(self.host_bltn_opts.generated_config) > 0

    def test_load_remediation(self, running_config, generated_config):
        self.host.load_running_config(running_config)
        self.host.load_generated_config(generated_config)
        self.host.remediation_config()
        self.host_bltn_opts.load_running_config(running_config)
        self.host_bltn_opts.load_generated_config(generated_config)
        self.host_bltn_opts.remediation_config()

        assert len(self.host.remediation_config().children) > 0
        assert len(self.host_bltn_opts.remediation_config().children) > 0

    def test_load_rollback(self, running_config, generated_config):
        self.host.load_running_config(running_config)
        self.host.load_generated_config(generated_config)
        self.host.rollback_config()
        self.host_bltn_opts.load_running_config(running_config)
        self.host_bltn_opts.load_generated_config(generated_config)
        self.host_bltn_opts.rollback_config()

        assert len(self.host.rollback_config().children) > 0
        assert len(self.host_bltn_opts.rollback_config().children) > 0

    def test_future_config(
        self, running_config, generated_config, tags_ios, future_config
    ):
        self.host.load_running_config(running_config)
        self.host.load_generated_config(generated_config)
        self.host.load_tags(tags_ios)
        future_cfg = self.host.future_config({"safe"})

        assert (
            "\n".join(
                [line.cisco_style_text() for line in future_cfg.all_children_sorted()]
            )
            == future_config
        )

    def test_load_tags(self, tags_ios):
        self.host.load_tags(tags_ios)
        assert len(self.host.hconfig_tags) > 0

    def test_filter_remediation(self, running_config, generated_config, tags_ios):
        self.host.load_running_config(running_config)
        self.host.load_generated_config(generated_config)
        self.host.load_tags(tags_ios)

        rem1 = self.host.remediation_config_filtered_text(set(), set())
        rem2 = self.host.remediation_config_filtered_text({"safe"}, set())

        assert rem1 != rem2
