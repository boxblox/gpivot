$title A Transportation Problem (TRNSPORT,SEQ=1)

$onText
This problem finds a least cost shipping schedule that meets
requirements at markets and supplies at factories.


Dantzig, G B, Chapter 3.3. In Linear Programming and Extensions.
Princeton University Press, Princeton, New Jersey, 1963.

This formulation is described in detail in:
Rosenthal, R E, Chapter 2: A GAMS Tutorial. In GAMS: A User's Guide.
The Scientific Press, Redwood City, California, 1988.

The line numbers will not match those in the book because of these
comments.

Keywords: linear programming, transportation problem, scheduling
$offText

Set
   i 'canning plants' / seattle,  san-diego /
   j 'markets'        / new-york, chicago, topeka /;

Set scn "scenario number" / 1*10 /;

Parameter
   a(i) 'capacity of plant i in cases'
        / seattle    350
          san-diego  600 /

   b(j) 'demand at market j in cases'
        / new-york   325
          chicago    300
          topeka     275 /;

* Table d(i,j) 'distance in thousands of miles'
*            new-york  chicago  topeka
* seattle         2.5      1.7     1.8
* san-diego       2.5      1.8     1.4;

Parameter d(i,j) 'distance in thousands of miles';

Scalar f 'freight in dollars per case per thousand miles' / 90 /;

Parameter c(i,j) 'transport cost in thousands of dollars per case';

Variable
   x(i,j) 'shipment quantities in cases'
   z      'total transportation costs in thousands of dollars';

Positive Variable x;

Equation
   cost      'define objective function'
   supply(i) 'observe supply limit at plant i'
   demand(j) 'satisfy demand at market j';

cost..      z =e= sum((i,j), c(i,j)*x(i,j));

supply(i).. sum(j, x(i,j)) =l= a(i);

demand(j).. sum(i, x(i,j)) =g= b(j);

Model transport / all /;


Parameter x_scn(scn,*,*,*);



loop(scn,

* create some fake uncertainity in distances between supply & demand regions
  d(i,"new-york") = uniform(2.4,2.6);
  d(i,"chicago") = uniform(1.6,1.9);
  d(i,"topeka") = uniform(1.3,1.9);

  c(i,j) = f*d(i,j)/1000;

  solve transport using lp minimizing z;

  x_scn(scn,i,j,'.L') = x.L(i,j);
  x_scn(scn,i,j,'.M') = x.M(i,j);

  );

execute_unload "trnsport_pivot_output.gdx";


FILE query /'%gams.scrdir%query.txt'/;

PUT query;
PUT " data=='.L' "
PUTCLOSE query;

* an example with querying and a pivot operation
EXECUTE "python3 gpivot.py --querydir %gams.scrdir% --gdxfile trnsport_pivot_output.gdx --param x_scn --index supply demand --header scn supply demand data --aggfunc np.mean --outfile pivot_1 --eps 1e-10";

* an example with just a pivot operation
EXECUTE "python3 gpivot.py --querydir %gams.scrdir% --gdxfile trnsport_pivot_output.gdx --param x_scn --header scn supply demand data --aggfunc np.mean --outfile pivot_2 --eps 1e-10";
