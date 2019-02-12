# gpivot
gpivot enables querying and pivoting of a high dimensional GAMS parameter from within a .gms model file.  gpivot will read in data from a source GDX file.  The query definition uses the pandas .query method of creating a human readable query structure rather than more traditional pandas syntax  The function outputs csvs of the results.  More information on creating these queries can be found here: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html. Due to poor string handling within GAMS the query is written to a scratch file which is later removed after the .gms model file completes.

# Use
An example file of the 'execute' command is include with this repo.  Embedded within this function is the gdx_reader class from 'gdxrw'.

# Requirements
Python 3, GAMS API, Pandas
