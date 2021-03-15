# CV
[![Update publications](https://github.com/arjunsavel/CV/actions/workflows/update_pubs.yml/badge.svg)](https://github.com/arjunsavel/CV/actions/workflows/update_pubs.yml) [![Add JOSS Reviews](https://github.com/arjunsavel/CV/actions/workflows/add_review_nums.yml/badge.svg)](https://github.com/arjunsavel/CV/actions/workflows/add_review_nums.yml)

Arjun Savel's CV, [linked with Overleaf](https://www.overleaf.com/). See the compiled version on the [corresponding website](https://arjunsavel.github.io/).

The formatting of this CV is based on @davidwhogg's, and the implementation of continuous integration was inspired by that of @dfm.

## Process
Every 24 hours, the `add_review_nums` workflow is run. This scrapes JOSS for the number of reviews I've conducted, writes this number to the main tex file, and commits the changes. 

Additionally, `scrape_ads` is run, which pulls my publications & their citations from [NASA ADS](https://ui.adsabs.harvard.edu/). These are aggregated, formatted, and written to a tex file. 
