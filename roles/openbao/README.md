Role Name
=========

This role installs and configures OpenBao as a service and prepares a cluster-ready configuration for one or more hosts. It supports:

- installation from the official OpenBao package repository
- installation from a released binary tarball
- configuration of the runtime paths, TLS settings, API/cluster addresses, and Raft storage
- optional AWS KMS auto-unseal through the `awskms` seal configuration

Requirements
------------

- Ansible on the managed host
- `systemd` for service management
- package manager access for repository installs or the ability to download the OpenBao binary distribution
- when using AWS KMS seal, valid AWS credentials and KMS permissions for the target account

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
| `openbao_repository_configuration_file_debian` | `"files/openbao.sources"` | Debian repository source file. |
| `openbao_repository_configuration_file_redhat` | `"files/openbao.repo"` | RedHat repository source file. |
| `openbao_repository_configuration_file_src` | OS-dependent | Repository source file to copy to the host. |
| `openbao_repository_configuration_file_dest` | OS-dependent | Repository configuration directory. |
| `openbao_repository_package_name` | OS-dependent versioned package | Package name to install from the repository. |
| `openbao_binary_installation` | `false` | Use the binary installation flow instead of the package repository flow. |
| `openbao_binary_package_download_directory_url` | `"https://github.com/openbao/openbao/releases/download"` | Base URL for release artifacts. |
| `openbao_binary_package_download_url` | `"{{ openbao_binary_package_download_directory_url }}/v{{ openbao_version }}/openbao_{{ openbao_version }}_linux_amd64.tar.gz"` | Archive URL for the OpenBao binary distribution. |
| `openbao_binary_package_gpg_key_verification` | `true` | Enable GPG verification for the downloaded binary. |
| `openbao_binary_package_gpg_package_name` | `"gpg"` | Package required for GPG verification. |
| `openbao_binary_package_gpg_public_key_file` | `"files/openbao-gpg-pub-20240618.asc"` | Local public key used to verify the archive. |
| `openbao_binary_package_download_gpg_key_url` | `"{{ openbao_binary_package_download_url }}.gpgsig"` | URL of the detached GPG signature file. |
| `openbao_configuration_base_path` | `/etc/openbao or /opt/openbao` | Root directory for runtime and configuration. |
| `openbao_configuration_data_path` | `/opt/openbao` | Base path used for cluster data and systemd configuration. |
| `openbao_configuration_runtime_path` | `"{{ openbao_configuration_base_path }}/bin"` | Directory containing the OpenBao executable. |
| `openbao_configuration_config_path` | `"{{ openbao_configuration_base_path }}"` | Directory containing the service configuration and environment files. |
| `openbao_configuration_environment_file_name` | `"openbao.env"` | Name of the environment file rendered by the role. |
| `openbao_configuration_config_file_name` | `"openbao.hcl"` | Name of the main HCL configuration file. |
| `openbao_configuration_tls_path` | `"{{ openbao_configuration_base_path }}/tls"` | Directory used for TLS material. |
| `openbao_configuration_tls_cert_file` | `"{{ openbao_configuration_tls_path }}/server.crt"` | Server certificate file. |
| `openbao_configuration_tls_key_file` | `"{{ openbao_configuration_tls_path }}/server.key"` | Server private key file. |
| `openbao_configuration_tls_ca_file` | `"{{ openbao_configuration_tls_path }}/ca.crt"` | CA certificate file. |
| `openbao_configuration_data_storage_raft_path` | `"{{ openbao_configuration_data_path }}/data"` | Raft storage path. |
| `openbao_configuration_data_audit_path` | `"{{ openbao_configuration_data_path }}/audit"` | Audit log path. |
| `openbao_configuration_data_log_path` | `"{{ openbao_configuration_data_path }}/log"` | Log directory. |
| `openbao_configuration_data_systemd_path` | `"{{ openbao_configuration_data_path }}/.config/systemd/user"` | Directory for the systemd unit file. |
| `openbao_configuration_data_systemd_unit_name` | `"openbao.service"` | Name of the rendered unit file. |
| `openbao_configuration_api_port` | `8200` | OpenBao API listener port. |
| `openbao_configuration_api_addr` | `"http://{{ inventory_hostname }}:{{ openbao_configuration_api_port }}"` | External URL advertised for the API endpoint. |
| `openbao_configuration_cluster_port` | `8201` | OpenBao cluster listener port. |
| `openbao_configuration_cluster_addr` | `"http://{{ inventory_hostname }}:{{ openbao_configuration_cluster_port }}"` | URL advertised for clustering. |
| `openbao_seal_awskms_configuration` | `region: "us-east-1"`, `kms_key_id: ""`, etc. | AWS KMS seal configuration map passed into the `seal "awskms"` block. |

AWS KMS Seal configuration
-------------------------

The role exposes `openbao_seal_awskms_configuration` as a dictionary that can be rendered into the OpenBao seal stanza. The default structure is:

    openbao_seal_awskms_configuration:
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

These keys match the options documented by OpenBao for the `awskms` seal backend.

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
        openbao_seal_awskms_configuration:
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

[AGPL-3.0-or-later](https://github.com/adfinis/ansible-collection-openbao/blob/main/LICENSE)

Author Information
------------------

* Simon Nussbaum <simon.nussbaum@adfinis.com>
