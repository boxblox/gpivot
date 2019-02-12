import pandas as pd
import numpy as np
import argparse
import sys
from gams import *

class gdx_reader:
    def __init__(self,gdxfile):
        ws = GamsWorkspace(working_directory = "./")
        self.db = ws.add_database_from_gdx(gdxfile)


    def getSymbols(self):
        symbols = []
        for i in self.db:
            symbols.append(i.name)
        return symbols


    def getSymbolTypes(self,**kwargs):
        name = kwargs.get('name', None)

        if name is None:
            t = self.getSymbols()
        else:
            if type(name) == str:
                t = [name]
            elif type(name) == list:
                t = name
            else:
                raise Exception('kwarg must be of type str or list')

        types = {}
        for i in t:
            types[i] = str(type(self.db[i])).split("'")[1].split('.')[-1]
        return types


    def rgdx(self,**kwargs):
        name = kwargs.get('name', None)

        if name is None:
            t = self.getSymbolTypes()
        else:
            if type(name) == str:
                t = self.getSymbolTypes(name=[name])
            elif type(name) == list:
                t = self.getSymbolTypes(name=name)
            else:
                raise Exception('kwarg must be of type str or list')

        d = {}
        for i in t.keys():
            d[i] = {}
            if t[i] == 'GamsSet':
                if self.db[i].dimension == 1:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['elements'] = [rec.keys[0] for rec in self.db[i]]

                else:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['elements'] = [tuple(rec.keys) for rec in self.db[i]]


            elif t[i] == 'GamsParameter':
                if self.db[i].dimension == 0:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['values'] = self.db[i].first_record().value


                elif self.db[i].dimension == 1:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text

                    d[i]['values'] = {}
                    d[i]['values']['domain'] =  [rec.keys[0] for rec in self.db[i]]
                    d[i]['values']['data'] = [rec.value for rec in self.db[i]]


                else:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text

                    d[i]['values'] = {}
                    d[i]['values']['domain'] =  [tuple(rec.keys) for rec in self.db[i]]
                    d[i]['values']['data'] = [rec.value for rec in self.db[i]]


            elif t[i] == 'GamsVariable':
                if self.db[i].dimension == 0:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['vartype'] = self.db[i].vartype

                    d[i]['values'] = {}
                    d[i]['values']['domain'] =  []
                    d[i]['values']['lower'] = self.db[i].first_record().lower
                    d[i]['values']['level'] = self.db[i].first_record().level
                    d[i]['values']['upper'] = self.db[i].first_record().upper
                    d[i]['values']['scale'] = self.db[i].first_record().scale
                    d[i]['values']['marginal'] = self.db[i].first_record().marginal


                elif self.db[i].dimension == 1:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['vartype'] = self.db[i].vartype

                    d[i]['values'] = {}
                    d[i]['values']['domain'] =  [rec.keys[0] for rec in self.db[i]]
                    d[i]['values']['lower'] = [rec.lower for rec in self.db[i]]
                    d[i]['values']['level'] = [rec.level for rec in self.db[i]]
                    d[i]['values']['upper'] = [rec.upper for rec in self.db[i]]
                    d[i]['values']['scale'] = [rec.scale for rec in self.db[i]]
                    d[i]['values']['marginal'] = [rec.marginal for rec in self.db[i]]

                else:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['vartype'] = self.db[i].vartype

                    d[i]['values'] = {}
                    d[i]['values']['domain'] =  [tuple(rec.keys) for rec in self.db[i]]
                    d[i]['values']['lower'] = [rec.lower for rec in self.db[i]]
                    d[i]['values']['level'] = [rec.level for rec in self.db[i]]
                    d[i]['values']['upper'] = [rec.upper for rec in self.db[i]]
                    d[i]['values']['scale'] = [rec.scale for rec in self.db[i]]
                    d[i]['values']['marginal'] = [rec.marginal for rec in self.db[i]]



            elif t[i] == 'GamsEquation':
                if self.db[i].dimension == 0:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text

                    d[i]['values'] = {}
                    d[i]['values']['domain'] =  []
                    d[i]['values']['lower'] = self.db[i].first_record().lower
                    d[i]['values']['level'] = self.db[i].first_record().level
                    d[i]['values']['upper'] = self.db[i].first_record().upper
                    d[i]['values']['scale'] = self.db[i].first_record().scale
                    d[i]['values']['marginal'] = self.db[i].first_record().marginal



                elif self.db[i].dimension == 1:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text

                    d[i]['values'] = {}
                    d[i]['values']['domain'] =  [rec.keys[0] for rec in self.db[i]]
                    d[i]['values']['lower'] = [rec.lower for rec in self.db[i]]
                    d[i]['values']['level'] = [rec.level for rec in self.db[i]]
                    d[i]['values']['upper'] = [rec.upper for rec in self.db[i]]
                    d[i]['values']['scale'] = [rec.scale for rec in self.db[i]]
                    d[i]['values']['marginal'] = [rec.marginal for rec in self.db[i]]

        if len(t) == 1:
            return d[list(t.keys())[0]]
        else:
            return d

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--gdxfile', default='out.gdx', type=str)
    parser.add_argument('--param', default='dude', type=str)
    parser.add_argument('--index', nargs='*')
    parser.add_argument('--columns', nargs='*')
    parser.add_argument('--querydir', type=str)
    parser.add_argument('--aggfunc', default='np.mean', type=str)
    parser.add_argument('--header', nargs='*', type=str)
    parser.add_argument('--outfile', default='out', type=str)
    parser.add_argument('--eps', default=1e-10, type=float)

    args = parser.parse_args()

    gdxin = gdx_reader(args.gdxfile)
    r = gdxin.rgdx(name=args.param)


    # only allow parameters at this point
    if r['type'] != 'GamsParameter':
        raise Exception('pivot object must be type GamsParameter')


    df = pd.DataFrame(data=r['values']['domain'])
    df['value'] = r['values']['data']

    cols = {i:args.header[i] for i in range(len(args.header))}
    df.rename(columns=cols, inplace=True)


    # assign very small numbers to zero
    df.loc[df[(df['value'] <= args.eps) & (df['value'] >= -args.eps)].index, 'value'] = 0


    df.to_csv('raw_' + args.outfile + '.csv')

    # read query from querydir
    with open(args.querydir + 'query.txt') as fp:
        query = fp.readline()


    # query your dataframe, reset index, and write out a csv
    df.query(query, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv('q_' + args.outfile + '.csv')

    print('**** ' + args.param + ' query successful ****')


    # create pivot table from queried dataframe and write out csv
    if args.index != None or args.columns != None:
        t = pd.pivot_table(df, values=['value'], index=args.index, columns=args.columns)
        # t.columns = t.columns.droplevel()
        # t.columns = t.columns.values
        t.reset_index(inplace=True)
        t.to_csv('p_' + args.outfile + '.csv')

        print('**** ' + args.param + ' pivot successful ****')
