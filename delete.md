# ===============================
# DELETE SYSTEM (JOURNAL) LOGS
# ===============================

# Delete logs older than 1 hour
sudo journalctl --vacuum-time=1h

# Delete logs older than 10 minutes
sudo journalctl --vacuum-time=10m

# Limit logs to 100MB
sudo journalctl --vacuum-size=100M


# ===============================
# DELETE TRADITIONAL LOG FILES
# ===============================

# Delete log files older than 1 hour
sudo find /var/log -type f -mmin +60 -delete

# Delete ALL log files (dangerous)
sudo rm -rf /var/log/*

# Clear log files safely (keep files)
sudo truncate -s 0 /var/log/*.log


# ===============================
# CLEAR USER HISTORY
# ===============================

# Clear current terminal history
history -c

# Delete saved history
rm -f ~/.bash_history


# ===============================
# FULL LOG CLEAN (AGGRESSIVE)
# ===============================

echo "Clearing all logs..." && \
sudo journalctl --rotate && \
sudo journalctl --vacuum-time=1s && \
sudo rm -rf /var/log/* && \
sudo mkdir -p /var/log && \
sudo systemctl restart systemd-journald && \
history -c && rm -f ~/.bash_history && \
echo "All logs cleared."