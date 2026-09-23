# Transport and authentication failures

Classify the failing layer before changing the write path:

| Observation | What it establishes | Next read-only check |
| --- | --- | --- |
| DNS or connection fails inside a sandbox | This environment could not reach the host. | Check the same configured remote in an authorized network context. |
| Host reachable, SSH agent declines signing | That signature attempt failed; key availability may be transient. | Retry the configured remote once after checking agent availability. |
| SSH authentication rejected by host | The presented identity did not authenticate for this host. | Check intended host/account and a read-only remote query. |
| HTTPS authentication rejected | That HTTPS credential did not authenticate. | Check intended account through established tooling without revealing credentials. |

Use the normal configured `origin` for a read-only retry after a transient failure. Do not infer a
permanent SSH outage from one agent refusal or conflate sandbox DNS with provider failure. If a
different URL, transport, account, or API write path is still needed, identify its exact repository
and branch. Confirm that existing operator authorization covers the changed method and identity,
or obtain agreement before the write. HTTPS is an available alternative when authorized, not
categorically forbidden.

Never print private keys, tokens, credential-helper contents, or credential-bearing remote URLs.
After an uncertain write, use a read-only remote-ref query to determine whether it already landed
before trying again.
