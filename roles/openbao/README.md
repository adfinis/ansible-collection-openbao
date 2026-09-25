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
| `openbao_version` | `"2.6.1"` | OpenBao version to install or match. |
| `openbao_user_creation` | `false` | Create the OS user used to run OpenBao. |
| `openbao_user_name` | `"openbao"` | Local OpenBao system user. |
| `openbao_user_group_name` | `"{{ openbao_user_name }}"` | Local OpenBao system group. |
| `openbao_user_home` | `"{{ openbao_configuration_base_path }}"` | User home directory. |
| `openbao_user_home_creation` | `false` | Create the user home directory. |
| `openbao_service_disabled` | `false` | Disable the OpenBao service at startup. |
| `openbao_binary_installation` | `false` | Use the binary distribution flow instead of the OS package repository. |
| `openbao_binary_architecture` | `{{ 'amd64' if ansible_facts.architecture == 'x86_64' else ansible_facts.architecture }}` | CPU architecture used for binary selection. |
| `openbao_binary_package_name` | `{{ 'openbao_' ~ openbao_version ~ '_linux_' ~ openbao_binary_architecture ~ '.tar.gz' }}` | Archive name for the released binary package. |
| `openbao_binary_package_download_directory_url` | `"https://github.com/openbao/openbao/releases/download"` | Base URL for release artifacts. |
| `openbao_binary_package_download_url` | `{{ openbao_binary_package_download_directory_url ~ '/v' ~ openbao_version ~ '/' ~ openbao_binary_package_name }}` | Full URL to the release archive. |
| `openbao_binary_package_gpg_key_verification` | `true` | Verify the downloaded binary with GPG. |
| `openbao_binary_package_gpg_package_name` | `"gpg"` | Package required for GPG verification. |
| `openbao_binary_package_gpg_public_key_url` | `"https://openbao.org/assets/openbao-gpg-pub-20240618.asc"` | Public GPG key URL used to verify the archive. |
| `openbao_binary_package_download_gpg_key_url` | `"{{ openbao_binary_package_download_url }}.gpgsig"` | Detached signature URL for the release archive. |
| `openbao_configuration_base_path` | `{{ '/etc/openbao' if openbao_binary_installation == false else '/opt/openbao' }}` | Root directory for runtime and configuration files. |
| `openbao_configuration_data_path` | `"/opt/openbao"` | Base path used for runtime, data, logs, and systemd configuration. |
| `openbao_configuration_runtime_path` | `"{{ openbao_configuration_base_path }}/bin"` | Directory containing the OpenBao executable. |
| `openbao_configuration_config_path` | `"{{ openbao_configuration_base_path }}"` | Directory containing the main config and environment files. |
| `openbao_configuration_config_template_file_path` | `"openbao.hcl.j2"` | Template used to render the HCL config file. |
| `openbao_configuration_config_file_name` | `"openbao.hcl"` | Name of the main HCL configuration file. |
| `openbao_configuration_environment_file_name` | `"openbao.env"` | Name of the environment file rendered on the host. |
| `openbao_configuration_environment_template_file_path` | `"openbao.env.j2"` | Template used to render the environment file. |
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
| `openbao_repository_name` | `"openbao"` | Repository name used by the package manager. |
| `openbao_repository_description` | `"OpenBao community repository"` | Repository description for RedHat/CentOS. |
| `openbao_repository_url` | `OS-dependent` | Repository URL for the target OS. |
| `openbao_repository_package_name` | `OS-dependent` | Package name to install from the repository. |
| `openbao_repository_components` | `"main"` | Repository components for Debian. |
| `openbao_repository_suites` | `"stable"` | Repository suites for Debian. |
| `openbao_repository_types` | `"deb"` | Repository types for Debian. |
| `openbao_repository_signature` | `"{{ openbao_binary_package_gpg_public_key_url }}"` | Repository GPG signature URL used by Debian. |
| `openbao_repository_gpgkey` | `"{{ openbao_binary_package_gpg_public_key_url }}"` | Repository GPG key URL used by RedHat. |
| `openbao_repository_gpgcheck` | `true` | Enable GPG checking for repository packages. |
| `openbao_repository_repo_gpgcheck` | `false` | Enable GPG checking for repository metadata. |
| `openbao_repository_enabled` | `true` | Enable the repository on RedHat-based systems. |
| `openbao_repository_sslverify` | `true` | Verify SSL certificates for the configured repo. |
| `openbao_repository_sslcacert` | `"/etc/pki/tls/certs/ca-bundle.crt"` | CA bundle path used for repository SSL verification. |
| `openbao_repository_metadata_expire` | `300` | Repository metadata expiration time in seconds. |

Seal configuration
------------------

The role exposes several `openbao_configuration_seal_*` dictionaries. Only define the backend you want to use and leave the others empty. Supported backends are `static`, `awskms`, `azurekeyvault`, `gcpckms`, `transit`, `pkcs11`, `ocikms`, `alicloudkms`, and `aead`.

Static seal (test values — do not use in production):

    openbao_configuration_seal_static:
      current_key_id: "test-1"
      current_key: "qU1Qtq04971uTpAJ6xiR6MdDJzUYcDJ2T5gx7Ofrrzw="

Example with the options for the `awskms` seal backend:

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

Only enable one seal backend in production. See the role defaults for the current structures of the supported backends.

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

Example Testlab Setup
---------------------

The following instructions show how to setup a testlab installation on VMs or on bare metal.

> ⚠️ THIS IS FOR TESTING ONLY AND SHALL NOT BE USED IN RPODUCTION ⚠️

**Requirements:**

- 1 or more hosts with a redhat or debian based distribution installed
- All hosts accessible via SSH
- All hosts resolve in DNS

**Instructions:**

1. Create an inventory file `inventory` similar to the following example

        testlab:
          hosts:
            host1.test.lab
            host2.test.lab
            host3.test.lab

2. Create a playbook file `playbook.yml` similar

        - name: Install openbao
          vars:
            openbao_configuration_tls_cert_file_src: 'tls.crt'
            openbao_configuration_tls_client_ca_file_src: 'CA.crt'
            openbao_configuration_tls_key_file_src: 'tls.key'
            openbao_configuration_seal_static:
              current_key_id: "test-1"
              current_key: "qU1Qtq04971uTpAJ6xiR6MdDJzUYcDJ2T5gx7Ofrrzw="
          hosts: testlab
          roles:
            - role: openbao

3. Generate Root CA key and certificate

        openssl req -x509 \
        -newkey rsa:4096 \
        -out CA.crt \
        -keyout CA.key \
        -subj "/O=OpenBao/CN=Root CA"
        -days 1095 # valid 3 years

4. Generate server key and issue certificate signed by the Root CA

        openssl req -new \
        -CA CA.crt \
        -CAkey CA.key \
        -out tls.crt \
        -keyout tls.key \
        -newkey rsa:4096 \
        -nodes \
        -sha256 \
        -x509 \
        -subj "/O=OpenBao/CN=OpenBao" \
        -addext "basicConstraints = CA:false" \
        -addext "subjectAltName = DNS:*.test.lab" \
        -days 90 # 3 months

5. Run Ansible playbook

        ansible-playbook -i inventory playbook.yml

6. Initialize OpenBao on one host

        export BAO_ADDR=https://localhost:8200
        export BAO_SKIP_VERIFY=1
        bao operator init

    Expected output:

        Recovery Key 1: 9GZ9OZHOKeLfmjOON6un05FLm999/lGvmXrRe5OuxDhs
        Recovery Key 2: sPaFUb+29P03moGV3nVx86I0IDIqxMAk4NIbcSZSyia2
        Recovery Key 3: xqNljeF4LrPd8kMs6uMsm/lAxxU7jraXuyEkFC7ITE5u
        Recovery Key 4: i1182f3PRv+fTCtecqwyd1bjT4u8nh/txHKHj1RkDWzL
        Recovery Key 5: qzbQJqAhCsv/XljdEMU42F21/HNoXKxgc4TFiVBqggIJ

        Initial Root Token: s.bIGBlmfdWO9fK7N0FZUcoAAe

        Success! Vault is initialized

        Recovery key initialized with 5 key shares and a key threshold of 3. Please
        securely distribute the key shares printed above.

7. Login to OpenBao using the `Initial Root Token`

        bao login

    expected output:

        Success! You are now authenticated. The token information displayed below is
        already stored in the token helper. You do NOT need to run "bao login" again.
        Future OpenBao requests will automatically use this token.

        Key                  Value
        ---                  -----
        token                s.bIGBlmfdWO9fK7N0FZUcoAAe
        token_accessor       OkAkGUeMqNNv2ZfVmll2HW7Y
        token_duration       ∞
        token_renewable      false
        token_policies       ["root"]
        identity_policies    []
        policies             ["root"]

8. Check OpenBao status on the host

        bao status

    Expected output:

        Key                      Value
        ---                      -----
        Seal Type                static
        Recovery Seal Type       shamir
        Initialized              false
        Sealed                   true
        Total Recovery Shares    0
        Threshold                0
        Unseal Progress          0/0
        Unseal Nonce             n/a
        Version                  2.6.1
        Commit Date              2026-07-22T14:22:20Z
        Storage Type             raft
        HA Enabled               true

9. Check OpenBao cluster members

        bao operator members

    Expected output:

        Host Name    API Address                     Cluster Address                 Active Node    Version    Upgrade Version    Last Echo
        ---------    -----------                     ---------------                 -----------    -------    ---------------    ---------
        host-1       https://host-1.test.lab:8200    https://host-1.test.lab:8201    true           2.6.1      2.6.1              n/a
        host-2       https://host-2.test.lab:8200    https://host-2.test.lab:8201    false          2.6.1      2.6.1              2026-09-25T09:56:19+02:00
        host-3       https://host-3.test.lab:8200    https://host-3.test.lab:8201    false          2.6.1      2.6.1              2026-09-25T09:56:19+02:00

> 💡
>
> Certificates can also be passed using environment variables `TLS_SERVER_KEY`, `TLS_SERVER_CERT` and `TLS_CLIENT_CA_CERT`. E.g. with the following `playbook.yml`
>
>     cat <<EOF > playbook.yml
>     - name: Install openbao
>       vars:
>         openbao_configuration_seal_static:
>           current_key_id: "test-1"
>           current_key: "qU1Qtq04971uTpAJ6xiR6MdDJzUYcDJ2T5gx7Ofrrzw="
>       hosts: testlab
>       roles:
>         - role: openbao
>     EOF
>
>     export TLS_SERVER_KEY="-----BEGIN PRIVATE KEY-----..."
>     export TLS_SERVER_CERT="-----BEGIN CERTIFICATE-----..."
>     export TLS_CLIENT_CA_CERT="-----BEGIN CERTIFICATE-----..."
>
>     ansible-playbook -i inventory playbook.yaml

License
-------

[AGPL-3.0-or-later](../../LICENSE)

Author Information
------------------

- Simon Nussbaum <simon.nussbaum@adfinis.com>
