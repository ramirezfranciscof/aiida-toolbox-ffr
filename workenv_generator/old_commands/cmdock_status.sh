#!/usr/bin/env bash

docker inspect --format "{{.State.Health.Status}}" quantum-mobile
