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

The role supports a broad set of variables for installation, runtime paths, TLS material, seal configuration, and repository setup. The defaults below reflect the current values in the role.

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `openbao_service_configuration_user_name` | `"openbao"` | Local OpenBao system user. |
| `openbao_service_configuration_user_group_name` | `"{{ openbao_service_configuration_user_name }}"` | Local OpenBao system group. |
| `openbao_service_configuration_systemd_unit_disabled` | `false` | Disable the OpenBao service at startup. |
| `openbao_configuration_base_path` | `{{ '/etc/openbao' if openbao_binary_installation == false else '/opt/openbao' }}` | Root directory for runtime and configuration files. |
| `openbao_configuration_data_path` | `"/opt/openbao"` | Base path used for runtime, data, logs, and systemd configuration. |
| `openbao_configuration_runtime_path` | `"{{ openbao_configuration_base_path }}/bin"` | Directory containing the OpenBao executable. |
| `openbao_configuration_config_path` | `"{{ openbao_configuration_base_path }}"` | Directory containing the main config and environment files. |
| `openbao_configuration_config_template_content` | `{{ lookup('file', openbao_configuration_config_template_file_path) }}` | File content loaded from the HCL template path. |
| `openbao_configuration_config_file_name` | `"openbao.hcl"` | Name of the main HCL configuration file. |
| `openbao_configuration_config_template_file_path` | `"openbao.hcl.j2"` | Path to the HCL config template file. |
| `openbao_configuration_environment_template_content` | `{{ lookup('file', openbao_configuration_environment_template_file_path) }}` | File content loaded from the environment template path. |
| `openbao_configuration_environment_file_name` | `"openbao.env"` | Name of the environment file rendered on the host. |
| `openbao_configuration_environment_template_file_path` | `"openbao.env.j2"` | Path to the environment template file. |
| `openbao_configuration_tls_path` | `"{{ openbao_configuration_data_path }}/tls"` | Directory for TLS material. |
| `openbao_configuration_tls_cert_content` | `{{ lookup('file', openbao_configuration_tls_cert_file_src) if openbao_configuration_tls_cert_file_src \| length > 0 else lookup('ansible.builtin.env', 'TLS_SERVER_CERT') }}` | PEM contents for the server certificate; reads a local file when `*_file_src` is set. |
| `openbao_configuration_tls_cert_file` | `{{ openbao_configuration_tls_path ~ '/' ~ openbao_configuration_tls_cert_file_src \| basename if openbao_configuration_tls_cert_file_src \| length > 0 else openbao_configuration_tls_path ~ '/server.crt' }}` | Server certificate location on disk. |
| `openbao_configuration_tls_cert_file_src` | `''` | Optional local source file for the server certificate. |
| `openbao_configuration_tls_key_content` | `{{ lookup('file', openbao_configuration_tls_key_file_src) if openbao_configuration_tls_key_file_src \| length > 0 else lookup('ansible.builtin.env', 'TLS_SERVER_KEY') }}` | PEM contents for the server private key; reads a local file when `*_file_src` is set. |
| `openbao_configuration_tls_key_file` | `{{ openbao_configuration_tls_path ~ '/' ~ openbao_configuration_tls_key_file_src \| basename if openbao_configuration_tls_key_file_src \| length > 0 else openbao_configuration_tls_path ~ '/server.key' }}` | Server private key location on disk. |
| `openbao_configuration_tls_key_file_src` | `''` | Optional local source file for the server private key. |
| `openbao_configuration_tls_client_ca_content` | `{{ lookup('file', openbao_configuration_tls_client_ca_file_src) if openbao_configuration_tls_client_ca_file_src \| length > 0 else lookup('ansible.builtin.env', 'TLS_CLIENT_CA_CERT') }}` | PEM contents for the client CA bundle; reads a local file when `*_file_src` is set. |
| `openbao_configuration_tls_client_ca_file` | `{{ openbao_configuration_tls_path ~ '/' ~ openbao_configuration_tls_client_ca_file_src \| basename if openbao_configuration_tls_client_ca_file_src \| length > 0 else openbao_configuration_tls_path ~ '/ca.crt' }}` | Client CA certificate location on disk. |
| `openbao_configuration_tls_client_ca_file_src` | `''` | Optional local source file for the client CA certificate. |
| `openbao_configuration_data_storage_raft_path` | `"{{ openbao_configuration_data_path }}/data"` | Raft storage directory. |
| `openbao_configuration_data_audit_path` | `"{{ openbao_configuration_data_path }}/audit"` | Audit log directory. |
| `openbao_configuration_data_log_path` | `"{{ openbao_configuration_data_path }}/log"` | Log directory. |
| `openbao_configuration_data_systemd_path` | `"{{ openbao_configuration_data_path }}/systemd"` | Directory for the generated systemd unit file. |
| `openbao_configuration_data_systemd_unit_name` | `"openbao.service"` | Name of the rendered systemd unit file. |
| `openbao_configuration_data_systemd_template_file_path` | `"openbao.service.j2"` | Systemd unit template used by the role. |
| `openbao_configuration_api_port` | `8200` | OpenBao API listener port. |
| `openbao_configuration_api_addr` | `https://{{ inventory_hostname ~ ':' ~ openbao_configuration_api_port }}` | URL advertised for the API endpoint. |
| `openbao_configuration_cluster_port` | `8201` | OpenBao cluster listener port. |
| `openbao_configuration_cluster_addr` | `https://{{ inventory_hostname ~ ':' ~ openbao_configuration_cluster_port }}` | URL advertised for clustering. |
| `openbao_configuration_seal_static` | `{}` | Static seal backend config for testing only. |
| `openbao_configuration_seal_awskms` | `{}` | AWS KMS seal backend config. |
| `openbao_configuration_seal_azurekeyvault` | `{}` | Azure Key Vault seal backend config. |
| `openbao_configuration_seal_gcpckms` | `{}` | Google Cloud KMS seal backend config. |
| `openbao_configuration_seal_transit` | `{}` | Transit seal backend config. |
| `openbao_configuration_seal_pkcs11` | `{}` | PKCS#11 seal backend config. |
| `openbao_configuration_seal_ocikms` | `{}` | OCI KMS seal backend config. |
| `openbao_configuration_seal_alicloudkms` | `{}` | Alibaba Cloud KMS seal backend config. |
| `openbao_configuration_seal_aead` | `{}` | AEAD seal backend config. |

Seal configuration
------------------

The role exposes several `openbao_service_configuration_seal_*` dictionaries. Only define the backend you want to use and leave the others empty. Supported backends are `static`, `awskms`, `azurekeyvault`, `gcpckms`, `transit`, `pkcs11`, `ocikms`, `alicloudkms`, and `aead`.

Static seal (test values — do not use in production):

    openbao_service_configuration_seal_static:
      current_key_id: "test-1"
      current_key: "qU1Qtq04971uTpAJ6xiR6MdDJzUYcDJ2T5gx7Ofrrzw="

Example with the options for the `awskms` seal backend:

    openbao_service_configuration_seal_awskms:
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

Only enable one seal backend in production. See the role defaults for the current structures of the supported backends.

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: openbao
      become: true
      vars:
        openbao_service_configuration_seal_awskms:
          region: "eu-central-1"
          kms_key_id: "arn:aws:kms:eu-central-1:123456789012:key/abcd1234-ef56-7890-abcd-ef1234567890"
          access_key: "{{ vault_aws_access_key }}"
          secret_key: "{{ vault_aws_secret_key }}"
          disable_renewal: false
      roles:
        - role: openbao.openbao_install
        - role: openbao.openbao_service_configuration

This example installs OpenBao from the repository, creates the service user, and configures AWS KMS auto-unseal for the cluster.

License
-------

[AGPL-3.0-or-later](../../LICENSE)

Author Information
------------------

- Simon Nussbaum <simon.nussbaum@adfinis.com>
