# Adfinis Openbao Collection

This repository contains the `adfinis.openbao` Ansible Collection. The collection contains roles to install and configure [OpenBao](https://www.openbao.org) clusters on servers and to back up OpenBao Raft storage.

Further configuration management that requires access to the OpenBao API and needs authentication is not supported. Please use OpenTofu or similar "state-aware" configuration management tools for this.

<!--start requires_ansible-->
<!--end requires_ansible-->

## External requirements

Some modules and plugins require external libraries. Please check the
requirements for each plugin or module you use in the documentation to find out
which requirements are needed.

## Included content

### Roles

| Role | Description |
| ---- | ----------- |
| [`adfinis.openbao.openbao_backup`](./roles/openbao_backup/) | Configures scheduled OpenBao Raft snapshots and optionally syncs them to S3-compatible storage |
| [`adfinis.openbao.openbao_install`](./roles/openbao_install/) | Install OpenBao from repository or tarball |
| [`adfinis.openbao.openbao_service_configuration`](./roles/openbao_service_configuration/) | Configures OpenBao as a service and prepares a cluster-ready configuration for one or more hosts |

## Using this collection

```bash
    ansible-galaxy collection install adfinis.openbao
```

You can also include it in a `requirements.yml` file and install it via
`ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
  - name: adfinis.openbao
```

To upgrade the collection to the latest available version, run the following
command:

```bash
ansible-galaxy collection install adfinis.openbao --upgrade
```

You can also install a specific version of the collection, for example, if you
need to downgrade when something is broken in the latest version (please report
an issue in this repository). Use the following syntax where `X.Y.Z` can be any
[available version](https://galaxy.ansible.com/adfinis/openbao):

```bash
ansible-galaxy collection install adfinis.openbao:==X.Y.Z
```

See
[Ansible Using Collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
for more details.

## Example Testlab Setup

The following instructions show how to setup a testlab installation on VMs or on bare metal.

> [!WARNING]
> THIS IS FOR TESTING ONLY AND SHALL NOT BE USED IN RPODUCTION

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
            openbao_service_configuration_tls_cert_file_src: 'tls.crt'
            openbao_service_configuration_tls_client_ca_file_src: 'CA.crt'
            openbao_service_configuration_tls_key_file_src: 'tls.key'
            openbao_service_configuration_seal_static:
              current_key_id: "test-1"
              current_key: "qU1Qtq04971uTpAJ6xiR6MdDJzUYcDJ2T5gx7Ofrrzw="
          hosts: testlab
          roles:
            - role: openbao_install
            - role: openbao_service_configuration
            - role: openbao_backup

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

> [!TIP]
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
>         - role: openbao_install
>         - role: openbao_service_configuration
>         - role: openbao_backup
>     EOF
>
>     export TLS_SERVER_KEY="-----BEGIN PRIVATE KEY-----..."
>     export TLS_SERVER_CERT="-----BEGIN CERTIFICATE-----..."
>     export TLS_CLIENT_CA_CERT="-----BEGIN CERTIFICATE-----..."
>
>     ansible-playbook -i inventory playbook.yaml

## Release notes

See the
[changelog](https://github.com/ansible-collections/adfinis.openbao/tree/main/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/matrix channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible collection development forum](https://forum.ansible.com/c/project/collection-development/27)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_requirements.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn)
- [News for Maintainers](https://forum.ansible.com/tag/news-for-maintainers)

## Licensing

GNU Affero General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/agpl-3.0.txt) to see the full text.
