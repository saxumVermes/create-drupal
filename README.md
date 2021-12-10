# Create Drupal

Manage multiple drupal sites with this simple script. Uses `docker compose` and `.env` to switch between available stacks.


## Getting Started

1. Copy `example.env.config.yaml`, name it `.env.config.yaml`. Fill it accordingly.
1. Run `./drupal create <stack_id> --nginx-port <some_port> --mysql-port <some_port>` to create a new stack
1. Run `./drupal compose up -d` to setup stack
1. Run `./drupal list` to available stacks

`./drupal compose` encapsulates `docker compose` to make the experience bit more seamless, same commands apply.

`./drupal --help` to check for available commands
