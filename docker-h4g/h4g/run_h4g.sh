#!/bin/bash
set -e

# Check the git connector was configured.
if [ ! -f /opt/perforce/git-connector/gconn.conf ]; then
    # Configure a git connecter if not yet.
    /opt/perforce/git-connector/bin/configure-git-connector.sh -n \
        --p4port $P4PORT \
        --super $P4USER \
        --superpassword $P4PASSWD \
        --graphdepot $GRAPHDEPOT \
        --gcuserp4password $GCUSERP4PASSW \
        --https
fi

# Monitor the log file
exec ls -1v --color=never /opt/perforce/git-connector/logs/* | xargs tail -f
