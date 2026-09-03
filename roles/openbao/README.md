Role: openbao
===============

Installs and configures OpenBao as a cluster-ready service on target hosts. It supports:

- installation from the official OpenBao package repository
- installation from a released binary tarball
- configuration of the runtime paths, TLS settings, API/cluster addresses, and Raft storage
- optional auto-unseal through seal configuration

Requirements
------------

- Ansible on the managed host
- `systemd` for service management
- package manager access for repository installs or the ability to download the OpenBao binary distribution

Role Variables
--------------

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `openbao_version` | `"2.6.1"` | OpenBao version to install or match. |
| `openbao_user_creation` | `false` | Create the operating system user used to run OpenBao. |
| `openbao_user_name` | `"openbao"` | Local OpenBao system user. |
| `openbao_user_group_name` | `"{{ openbao_user_name }}"` | Local OpenBao system group. |
| `openbao_user_home` | `"{{ openbao_configuration_base_path }}"` | User home directory. |
| `openbao_user_home_creation` | `false` | Create the user home directory. |
| `openbao_service_disabled` | `false` | Do not enable and start OpenBao service |
| `openbao_binary_installation` | `false` | Use the binary installation flow instead of the package repository flow. |
| `openbao_binary_architecture` | Architecture-dependent | CPU architecture for binary selection (amd64, arm64, etc.). |
| `openbao_binary_package_name` | OS-dependent | Binary package filename (e.g., `openbao_2.6.1_linux_amd64.tar.gz`). |
| `openbao_binary_package_download_directory_url` | `"https://github.com/openbao/openbao/releases/download"` | Base URL for release artifacts. |
| `openbao_binary_package_download_url` | Constructed from components | Full URL to download the OpenBao binary distribution. |
| `openbao_binary_package_gpg_key_verification` | `true` | Enable GPG verification for the downloaded binary. |
| `openbao_binary_package_gpg_package_name` | `"gpg"` | Package required for GPG verification. |
| `openbao_binary_package_gpg_public_key_file` | `"files/openbao-gpg-pub-20240618.asc"` | Local public key used to verify the archive. |
| `openbao_binary_package_download_gpg_key_url` | `"{{ openbao_binary_package_download_url }}.gpgsig"` | URL of the detached GPG signature file. |
| `openbao_configuration_base_path` | OS-dependent (defaults to `/etc/openbao` for package installs, `/opt/openbao` for binary installs) | Root directory for runtime and configuration. |
| `openbao_configuration_data_path` | `/opt/openbao` | Base path used for cluster data and systemd configuration. |
| `openbao_configuration_runtime_path` | `"{{ openbao_configuration_base_path }}/bin"` | Directory containing the OpenBao executable. |
| `openbao_configuration_config_path` | `"{{ openbao_configuration_base_path }}"` | Directory containing the service configuration and environment files. |
| `openbao_configuration_config_template_file_path` | `"openbao.hcl.j2"` | Jinja2 template file for HCL configuration. |
| `openbao_configuration_environment_file_name` | `"openbao.env"` | Name of the environment file rendered by the role. |
| `openbao_configuration_environment_template_file_path` | `"openbao.env.j2"` | Jinja2 template file for environment variables. |
| `openbao_configuration_config_file_name` | `"openbao.hcl"` | Name of the main HCL configuration file. |
| `openbao_configuration_tls_path` | `"{{ openbao_configuration_base_path }}/tls"` | Directory used for TLS material. |
| `openbao_configuration_tls_cert_file` | `"{{ openbao_configuration_tls_path }}/server.crt"` | Server certificate file. |
| `openbao_configuration_tls_key_file` | `"{{ openbao_configuration_tls_path }}/server.key"` | Server private key file. |
| `openbao_configuration_tls_ca_file` | `"{{ openbao_configuration_tls_path }}/ca.crt"` | CA certificate file. |
| `openbao_configuration_data_storage_raft_path` | `"{{ openbao_configuration_data_path }}/data"` | Raft storage path. |
| `openbao_configuration_data_audit_path` | `"{{ openbao_configuration_data_path }}/audit"` | Audit log path. |
| `openbao_configuration_data_systemd_path` | `"{{ openbao_configuration_data_path }}/systemd"` | Directory for the systemd unit file. |
| `openbao_configuration_data_systemd_unit_name` | `"openbao.service"` | Name of the rendered unit file. |
| `openbao_configuration_data_systemd_template_file_path` | `"openbao.service.j2"` | Jinja2 template file for systemd service unit. |
| `openbao_configuration_data_log_path` | `"{{ openbao_configuration_data_path }}/log"` | Log directory. |
| `openbao_configuration_api_port` | `8200` | OpenBao API listener port. |
| `openbao_configuration_api_addr` | Constructed from hostname and port | External URL advertised for the API endpoint. |
| `openbao_configuration_cluster_port` | `8201` | OpenBao cluster listener port. |
| `openbao_configuration_cluster_addr` | Constructed from hostname and port | URL advertised for clustering. |
| `openbao_configuration_seal_*` | `not set` | Configuration map passed into the `seal` block of given seal type. |

Seal configuration
------------------

The role exposes several `openbao_configuration_seal_*` dictionaries. Only define the backend you want to use; keep other dicts empty. Example structures matching the role defaults:

Static seal (test values — do not use in production):

    openbao_configuration_seal_static:
      current_key_id: "test-1"
      current_key: "qU1Qtq04971uTpAJ6xiR6MdDJzUYcDJ2T5gx7Ofrrzw="

Another example with the options for `awskms` seal backend:

    openbao_configuration_seal_awskms:
      region: "us-east-1"
      access_key: ""
      secret_key: ""
      session_token: ""
      kms_key_id: ""
      endpoint: ""
      iam_endpoint: ""
      sts_endpoint: ""
      role: ""
      disable_renewal: false
      lease_path: ""

Only enable one seal backend in production. See the role `defaults/main.yml` for the current default structures.

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: openbao
      become: true
      vars:
        openbao_binary_installation: false
        openbao_user_creation: true
        openbao_configuration_seal_awskms:
          region: "eu-central-1"
          kms_key_id: "arn:aws:kms:eu-central-1:123456789012:key/abcd1234-ef56-7890-abcd-ef1234567890"
          access_key: "{{ vault_aws_access_key }}"
          secret_key: "{{ vault_aws_secret_key }}"
          disable_renewal: false
      roles:
        - role: openbao.openbao

This example installs OpenBao from the repository, creates the service user, and configures AWS KMS auto-unseal for the cluster.

License
-------

[AGPL-3.0-or-later](../../LICENSE)

Author Information
------------------

- Simon Nussbaum <simon.nussbaum@adfinis.com>
