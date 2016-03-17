## Turboteam
Turboteam is a parser of chat logs from Naver's LINE chat program.

## Usage examples
Basic stats about the log (number of chat entries per day, per user, participating usernames)

```python3 tt.py --input-file log.txt```

Basic stats + frequency of a given term on a per-user basis

```python3 tt.py --input-file log.txt --density 'someword'```


Cover only a certain date range

```python3 tt.py --input-file log.txt --start-date 'YYYY/MM/DD'```

```python3 tt.py --input-file log.txt --start-date 'YYYY/MM/DD' --end-date 'YYYY/MM/DD'```
