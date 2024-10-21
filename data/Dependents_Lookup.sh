#! /bin/sh

curl -L https://sourcegraph.com/.api/src-cli/src_darwin_amd64 -o src
chmod +x src

# Get the path_repository argument
path_repository="$1"

src search -json 'context:global "leaderboard" select:repo count:all file:\.(html|md)' >"${path_repository}/GitHub.json"