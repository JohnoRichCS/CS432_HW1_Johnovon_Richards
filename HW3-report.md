# HW3 Report

## Q1. Get TimeMaps for Each URI-R

I used a local installation of MemGator to retrieve TimeMaps for the 500 URI-Rs collected in HW1. I used the required `-c` option to provide contact information and the `-a` option to use the alternate `archives.json` file. I saved the TimeMaps in JSON format in a separate `timemaps/` folder for later analysis.

To avoid overwhelming the archives, I inserted delays between requests while downloading the TimeMaps. The process completed successfully for all 500 URI-Rs.

## Q2. Analyze Mementos Per URI-R

The table below summarizes how many URI-Rs had different numbers of mementos.

| Mementos | URI-Rs |
|---:|---:|
| 0 | 220 |
| 1–10 | 164 |
| 11–20 | 74 |
| 21–30 | 10 |
| 31–50 | 10 |
| 51–100 | 7 |
| 101–500 | 7 |
| 501–1000 | 1 |
| 1001–2000 | 2 |
| 2001–5000 | 1 |
| 5001+ | 2 |

Out of the 500 URI-Rs, 220 had no mementos at all. This means that a large portion of the web pages I collected have not been archived, which matches what we discussed in class about how much of the web is still missing from archives.

The maximum number of mementos for a single URI-R was 7689. The two URI-Rs with the most mementos were:

- `https://web.archive.org/`
- `http://web.archive.org/`

The next highest URI-Rs were:

- `https://archive.is/` with 3069 mementos
- `https://archive-it.org/` with 1841 mementos
- `https://www.unc.edu/` with 1752 mementos
- `https://www.clemson.edu/` with 1007 mementos
- `https://www.odu.edu/` with 512 mementos

This did not completely surprise me because websites related to web archiving itself, such as the Internet Archive and Archive-It, are likely to be crawled and preserved very frequently. More visible university homepages also tend to receive better archival coverage than smaller or less popular pages.

One interesting finding is how uneven the archival coverage is. Many URI-Rs had zero mementos, while a very small number had extremely large numbers of mementos. This shows that web archiving is not evenly distributed across sites.