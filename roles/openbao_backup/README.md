# Role: openbao_backup

Configures scheduled backups of OpenBao integrated storage (Raft) snapshots.
The role installs `s3cmd`, configures an OpenBao agent for AppRole
authentication, and installs systemd services and a timer to create snapshots
and optionally sync them to S3-compatible storage.

## Requirements

- A host with `dnf` or `apt`, `systemd`, and Python 3 pip support.
- OpenBao with integrated storage (raft) as backend configured
- An OpenBao installation with the `bao` CLI available at
  `openbao_backup_bin_path`.
- OpenBao must be running and reachable at
  `openbao_backup_openbao_api_address`.
- An AppRole configured with permission to create Raft snapshots. Example configuration:

  ```json
  path "sys/storage/raft/snapshot" {
    capabilities = ["read"]
  }
  ```

- (Optional) An S3-compatible endpoint, bucket, and credentials.
- Privilege escalation to configure users, files, packages, and systemd.

## Role Variables

The role variables are prefixed with `openbao_backup_`. Credentials and
certificate content may be supplied directly through Ansible variables or
through the environment variables listed below. Environment lookups run on the
Ansible controller.

### OpenBao connection and AppRole

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `openbao_backup_openbao_api_address` | `'https://127.0.0.1:8200'` | OpenBao API address. |
| `openbao_backup_openbao_ca_certs_path` | `''` | Managed-host directory containing OpenBao CA certificates. |
| `openbao_backup_openbao_ca_certs_file_src` | `''` | Optional controller-side CA certificate file. If unset, the role reads `OPENBAO_BACKUP_BAO_CACERT`. |
| `openbao_backup_openbao_ca_certs_content` | Environment lookup | PEM content from the source file, or `OPENBAO_BACKUP_BAO_CACERT` when no file is specified. |
| `openbao_backup_agent_config_ca_certs_file` | Derived | Managed-host destination for the OpenBao CA certificate. |
| `openbao_backup_openbao_tls_server_name` | `""` | SNI name used for OpenBao TLS. |
| `openbao_backup_openbao_tls_skip_verify` | `false` | Skip OpenBao TLS certificate verification. Avoid enabling this in production. |
| `openbao_backup_agent_raft_snapshot_approle_role_id` | `''` | AppRole role ID used by the snapshot agent. |
| `openbao_backup_agent_raft_snapshot_approle_secret_id` | `'sensitive'` | AppRole secret ID used by the snapshot agent. Store this as an Ansible Vault secret. |
| `openbao_backup_agent_raft_snapshot_approle_role_id_file` | Derived | Managed-host destination for the AppRole role ID file. |
| `openbao_backup_agent_raft_snapshot_approle_secret_id_file` | Derived | Managed-host destination for the AppRole secret ID file. |
| `openbao_backup_agent_raft_snapshot_remove_secret_id_file_after_reading` | `true` | Remove the AppRole secret ID file after the agent reads it. |

The role writes AppRole credentials to files. The task that writes the secret
ID suppresses Ansible logging with `no_log`.

### Snapshots, scheduling, and retention

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `openbao_backup_raft_snapshot_dir` | `'/opt/bao/snapshots'` | Local directory for snapshot files. |
| `openbao_backup_raft_snapshot_file_name` | `{{ inventory_hostname_short }}-openbao-raft-$(date +%F-%H%M).snapshot` | Snapshot filename format. |
| `openbao_backup_raft_snapshot_retention_find_mode` | `'mtime'` | File age to check: `mtime` or `atime`. |
| `openbao_backup_raft_snapshot_retention_time` | `'+7'` | `find` age expression for snapshots to remove. |
| `openbao_backup_raft_snapshot_retention_find_action` | `'rm'` | `find -exec` action for expired snapshots. |
| `openbao_backup_raft_snapshot_systemd_dir` | `'/etc/systemd/system'` | Destination directory for snapshot systemd units. |
| `openbao_backup_raft_snapshot_systemd_timer_template` | `'templates/openbao-raft-snapshot.timer.j2'` | Template used to render the snapshot timer. |
| `openbao_backup_raft_snapshot_systemd_timer_name` | `'openbao-raft-snapshot.timer'` | Snapshot timer systemd unit name. |
| `openbao_backup_raft_snapshot_systemd_timer_service_template` | `'templates/openbao-raft-snapshot.service.j2'` | Template used to render the snapshot service. |
| `openbao_backup_raft_snapshot_systemd_timer_service_name` | `'openbao-raft-snapshot.service'` | One-shot snapshot systemd service name. |
| `openbao_backup_raft_snapshot_systemd_timer_onactivesec` | `'1s'` | Delay before the first scheduled snapshot. |
| `openbao_backup_raft_snapshot_systemd_timer_onunitactivesec` | `'1h'` | Interval between scheduled snapshots. |
| `openbao_backup_raft_snapshot_script_template` | `'templates/openbao-snapshot.sh.j2'` | Template used to render the snapshot script. |
| `openbao_backup_raft_snapshot_script_path` | `'/usr/local/bin/openbao-snapshot.sh'` | Destination path for the snapshot script. |

The default timer runs shortly after activation and then hourly. The one-shot
service creates a Raft snapshot, optionally syncs the snapshot directory to
S3, and removes expired local files.

### S3-compatible storage

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `openbao_backup_s3_sync` | `false` | Enable syncing snapshots to S3-compatible storage. |
| `openbao_backup_s3_config_dir` | `{{ openbao_backup_agent_config_dir }}` | Directory containing S3 client configuration. |
| `openbao_backup_s3_ca_certs_path` | `{{ openbao_backup_s3_config_dir }}` | Managed-host directory containing S3 CA certificates. |
| `openbao_backup_s3_ca_certs_file_src` | `''` | Optional controller-side CA certificate file for the S3 endpoint. |
| `openbao_backup_s3_ca_certs_content` | Environment lookup | PEM content from the source file, or `OPENBAO_BACKUP_S3_CA_CERT` when no file is specified. |
| `openbao_backup_s3_ca_certs_file` | Derived | Managed-host destination for the S3 CA certificate. |
| `openbao_backup_s3_config_path` | `{{ openbao_backup_s3_config_dir }}` | Path used for the `s3cmd` configuration file. |
| `openbao_backup_s3_access_key` | Environment lookup | S3 access key. |
| `openbao_backup_s3_expiry_days` | `90` | S3 object expiry setting; the current S3 client template uses a fixed 90-day value. |
| `openbao_backup_s3_host_base` | Environment lookup | S3-compatible endpoint hostname. |
| `openbao_backup_s3_host_bucket` | Environment lookup | Bucket name used as the snapshot destination. |
| `openbao_backup_s3_secret_key` | Environment lookup | S3 secret key. |

Unless set explicitly, the S3 access key, endpoint, bucket, and secret key are
read from `OPENBAO_BACKUP_S3_ACCESS_KEY`, `OPENBAO_BACKUP_S3_HOST_BASE`,
`OPENBAO_BACKUP_S3_HOST_BUCKET`, and `OPENBAO_BACKUP_S3_SECRET_KEY` in the
controller environment.

### Agent configuration and service identity

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `openbao_backup_bin_path` | `'/usr/bin'` | Directory containing the `bao` executable. |
| `openbao_backup_group` | `bao` | System group for the snapshot agent. |
| `openbao_backup_agent_config_dir` | `'/etc/openbao'` | OpenBao agent configuration directory. |
| `openbao_backup_agent_config_pid_file_name` | `'openbao-backup-agent.pid'` | OpenBao agent PID file name. |
| `openbao_backup_agent_config_pid_dir` | `{{ openbao_backup_agent_config_dir }}` | Directory containing the OpenBao agent PID file. |
| `openbao_backup_agent_config_run_dir` | `'openbao-backup-agent'` | systemd runtime directory for the OpenBao agent. |
| `openbao_backup_agent_config_listener_socket` | `{{ openbao_backup_agent_config_dir }}/agent.sock` | OpenBao agent listener Unix socket path. |
| `openbao_backup_agent_config_file` | `{{ openbao_backup_agent_config_dir }}/openbao_backup_agent.hcl` | OpenBao agent configuration file destination. |
| `openbao_backup_agent_config_file_template` | `'templates/openbao_backup_agent.hcl.j2'` | Template used to render the OpenBao agent configuration. |
| `openbao_backup_agent_systemd_dir` | `'/etc/systemd/system'` | Destination directory for the OpenBao agent systemd unit. |
| `openbao_backup_agent_systemd_service_template` | `'templates/openbao-backup-agent.service.j2'` | Template used to render the OpenBao agent systemd unit. |
| `openbao_backup_agent_systemd_service_name` | `'openbao-backup-agent.service'` | OpenBao agent systemd service name. |
| `openbao_backup_raft_snapshot_config_dir` | `{{ openbao_backup_agent_config_dir }}` | Configuration directory used by the snapshot service. |
| `openbao_backup_user` | `bao` | System user for the snapshot agent. |

Other role variables are available for overriding certificate destinations,
PID paths, template paths, and systemd unit details; see
[`defaults/main.yml`](./defaults/main.yml).

## Example

Store credentials in Ansible Vault and configure the endpoint and bucket in
inventory or a playbook:

```yaml
- name: Configure OpenBao snapshot backups
  hosts: openbao
  become: true
  roles:
    - role: adfinis.openbao.openbao_backup
      vars:
        openbao_backup_agent_raft_snapshot_approle_role_id: "db02de05-fa39-4855-059b-67221c5c2f63"
        openbao_backup_agent_raft_snapshot_approle_secret_id: "6a174c20-f6de-a53c-74d2-6018fcceff64"
        openbao_backup_s3_sync: true
        openbao_backup_s3_host_base: "s3.example.net"
        openbao_backup_s3_host_bucket: "openbao-snapshots"
        openbao_backup_s3_access_key: "TUOWAAA99023990001"
        openbao_backup_s3_secret_key: "sd/ceP_vbb#eDDDK"
```

## License

[AGPL-3.0-or-later](../../LICENSE)

## Author Information

- Simon Nussbaum <simon.nussbaum@adfinis.com>
