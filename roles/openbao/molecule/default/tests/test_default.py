import os
import testinfra.utils.ansible_runner

hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ.get('MOLECULE_INVENTORY_FILE')
).get_hosts('all')


def test_openbao_binary_present(host):
    f = host.file('/opt/openbao/bin/openbao')
    assert f.exists
    assert f.mode & 0o111


def test_systemd_unit_exists(host):
    # user systemd path depends on defaults; check for file presence
    unit = host.file('/opt/openbao/.config/systemd/user/openbao.service')
    assert unit.exists
