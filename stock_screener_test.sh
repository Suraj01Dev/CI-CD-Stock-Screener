#!/bin/bash
bandit --format json --output bandit-report.json --recursive stock_screener
if [[ $? -ne 0 ]]; then
	exit 1
fi

pylint stock_screener -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt 
exit 0
