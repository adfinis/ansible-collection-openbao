Role: openbao_install
=====================

Installs OpenBao on target hosts. It supports:

- installation from the official OpenBao package repository
- installation from a released binary tarball

Requirements
------------

- Ansible on the managed host
- package manager access for repository installs or the ability to download the OpenBao binary distribution

Role Variables
--------------

The role supports a broad set of variables for installation, runtime paths, TLS material, seal configuration, and repository setup. The defaults below reflect the current values in the role.

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `openbao_install_openbao_version` | `"2.6.1"` | OpenBao version to install or match. |
| `openbao_install_user_creation` | `false` | Create the OS user used to run OpenBao. |
| `openbao_install_user_name` | `"openbao"` | Local OpenBao system user. |
| `openbao_install_user_group_name` | `"{{ openbao_install_user_name }}"` | Local OpenBao system group. |
| `openbao_install_user_home` | `"/home/{{ openbao_install_user_name }}"` | User home directory. |
| `openbao_install_user_home_creation` | `false` | Create the user home directory. |
| `openbao_install_service_disabled` | `false` | Disable the OpenBao service at startup. |
| `openbao_install_binary_installation` | `false` | Use the binary distribution flow instead of the OS package repository. |
| `openbao_install_binary_architecture` | `{{ 'amd64' if ansible_facts.architecture == 'x86_64' else ansible_facts.architecture }}` | CPU architecture used for binary selection. |
| `openbao_install_binary_package_name` | `{{ 'openbao_' ~ openbao_version ~ '_linux_' ~ openbao_install_binary_architecture ~ '.tar.gz' }}` | Archive name for the released binary package. |
| `openbao_install_binary_package_download_directory_url` | `"https://github.com/openbao/openbao/releases/download"` | Base URL for release artifacts. |
| `openbao_install_binary_package_download_url` | `{{ openbao_install_binary_package_download_directory_url ~ '/v' ~ openbao_install_openbao_version ~ '/' ~ openbao_install_binary_package_name }}` | Full URL to the release archive. |
| `openbao_install_binary_package_gpg_key_verification` | `true` | Verify the downloaded binary with GPG. |
| `openbao_install_binary_package_gpg_package_name` | `"gpg"` | Package required for GPG verification. |
| `openbao_install_binary_package_gpg_public_key_url` | `"https://openbao.org/assets/openbao-gpg-pub-20240618.asc"` | Public GPG key URL used to verify the archive. |
| `openbao_install_binary_package_download_gpg_key_url` | `"{{ openbao_install_binary_package_download_url }}.gpgsig"` | Detached signature URL for the release archive. |
| `openbao_install_binary_destination_path` | `"/usr/local/bin"` | Destination path for the OpenBao binary installation. |
| `openbao_install_binary_systemd_template_file_path` | `"templates/openbao.service.j2"` | Jinja2 template file for systemd service unit. |
| `openbao_install_binary_systemd_path` | `"/etc/systemd/system"` | Directory for the systemd unit file. |
| `openbao_install_binary_systemd_unit_name` | `"openbao"` | Name of the systemd service unit file. |
| `openbao_install_binary_config_path` | `"/etc/openbao/"` | Directory containing the main config and environment files. |
| `openbao_install_binary_openbao_config_file_name` | `"openbao.hcl"` | Name of the main HCL configuration file. |
| `openbao_install_binary_systemd_environment_file_name` | `"openbao.env"` | Name of the environment file rendered on the host. |
| `openbao_install_debian_repository_package_name` | `{{ 'openbao=' ~ openbao_install_openbao_version }}` | Debian package specification used by the Debian repository task. |
| `openbao_install_debian_repository_name` | `"openbao"` | Debian repository name. |
| `openbao_install_debian_repository_url` | `"https://pkgs.openbao.org/deb/"` | Debian repository URL. |
| `openbao_install_debian_repository_components` | `"main"` | Debian repository components. |
| `openbao_install_debian_repository_suites` | `"stable"` | Debian repository suite. |
| `openbao_install_debian_repository_types` | `"deb"` | Debian repository type. |
| `openbao_install_debian_repository_signature` | `"{{ openbao_install_binary_package_gpg_public_key_url }}"` | Debian repository signing key URL. |
| `openbao_install_redhat_repository_name` | `"openbao"` | RedHat repository name. |
| `openbao_install_redhat_repository_description` | `"OpenBao community repository"` | RedHat repository description. |
| `openbao_install_redhat_repository_url` | `"https://pkgs.openbao.org/rpm/$basearch"` | RedHat repository base URL. |
| `openbao_install_redhat_repository_package_name` | `{{ 'openbao-' ~ openbao_install_openbao_version ~ '-1' }}` | RedHat package specification used by the RPM repository task. |
| `openbao_install_redhat_repository_repo_gpgcheck` | `false` | Enable repository metadata GPG checking for RedHat. |
| `openbao_install_redhat_repository_gpgcheck` | `true` | Enable package GPG checking for RedHat. |
| `openbao_install_redhat_repository_enabled` | `true` | Enable the RedHat repository. |
| `openbao_install_redhat_repository_gpgkey` | `"{{ openbao_install_binary_package_gpg_public_key_url }}"` | RedHat repository GPG key URL. |
| `openbao_install_redhat_repository_sslverify` | `true` | Verify SSL certificates for RedHat repository downloads. |
| `openbao_install_redhat_repository_sslcacert` | `"/etc/pki/tls/certs/ca-bundle.crt"` | CA bundle used for RedHat repository SSL verification. |
| `openbao_install_redhat_repository_metadata_expire` | `300` | RedHat repository metadata expiration time in seconds. |

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: openbao
      become: true
      roles:
        - role: openbao.openbao_install

This example installs OpenBao from the repository and creates the service user.

License
-------

[AGPL-3.0-or-later](../../LICENSE)

Author Information
------------------

- Simon Nussbaum <simon.nussbaum@adfinis.com>
