"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    return_dict = {}
    with open(filename, newline='') as csvfile:
        for line in csvfile:
            print(line)
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            row_key = row[keyfield]
            return_dict[row_key] = row
    print(return_dict)
    return return_dict

def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    code_convert_dict = {}
    print(codeinfo)
    print(codeinfo["codefile"],codeinfo["plot_codes"],codeinfo["separator"],codeinfo["quote"])
    cc_dict = read_csv_as_nested_dict(codeinfo["codefile"],
                                      codeinfo["plot_codes"],
                                      codeinfo["separator"],
                                      codeinfo["quote"])
##    for key,val in cc_dict.items():
##        code_convert_dict[key] = val[codeinfo["data_codes"]]
####    print("***",code_convert_dict,"***")
    return code_convert_dict

def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """file"],
                                      codeinfo["plot_codes"],
                                      codeinfo["separator"],
                                      codeinfo["quote"
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    net_plot_dict = {}
    recon_dict = {}
    recon_set = set()
    code_convert_dict = build_country_code_converter(codeinfo)
            
##    print("code convert dict",code_convert_dict)
##    print("plot countries",plot_countries)
##    print("GDP countries",gdp_countries)
##    print(recon_dict)
##    print(recon_set)
    
    for key,val in plot_countries.items():
        if key in code_convert_dict.keys():
            net_plot_dict[key] = val        
        elif key.lower() in code_convert_dict.keys():
            net_plot_dict[key.lower()] = val
##    print(net_plot_dict)

    for code2 in net_plot_dict.keys():
        if code_convert_dict[code2] in gdp_countries:
##            print(code2,code_convert_dict[code2])
            recon_dict[code2] = code_convert_dict[code2]
        else:
            recon_set.add(code2)
    print(recon_dict)
    print(recon_set)
    return recon_dict, recon_set


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                       gdpinfo["country_code"],
                                       gdpinfo["separator"],
                                       gdpinfo["quote"])
    code_dict = build_country_code_converter(codeinfo)
    
    
    pygal_gdp_dict = {}
    set_one = set()
    set_two = set()
    
##    print(code_dict)
##    print(plot_countries)
##    print(gdp_dict)
##    print("-------------")
    for pyplot_cd,gdp_code in plot_countries.items():
        if pyplot_cd in code_dict:
##            print(gdp_code,gdp_dict[gdp_code][year])
            ann_gdp = gdp_dict[gdp_code][year]
            if ann_gdp.isnumeric and len(ann_gdp):
                log_ann_gdp = math.log(float(ann_gdp),10)
                pygal_gdp_dict[pyplot_cd] = log_ann_gdp
            else:
                # this will be the 2nd set
                set_two.add(pyplot_cd)
        else:
            # this will be the 1st set
            set_one.add(pyplot_cd)
    for key,val in pygal_gdp_dict.items():
        print(key,val)
##    print(pygal_gdp_dict)
##    print("set 1: ",set_one)
##    print("set 2: ",set_two)
    
    return pygal_gdp_dict, set_one, set_two

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    return


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()

######################################################################
##gdpinfo = {
##    "gdpfile": "isp_gdp.csv",
####    "gdpfile": "gdptable1.csv",
##    "separator": ",",
##    "quote": '"',
##    "min_year": 1960,
##    "max_year": 2015,
##    "country_name": "Country Name",
##    "country_code": "Country Code"
##    }
codeinfo_code1 = {
    "codefile": "code1.csv",
    "separator": ",",
    "quote": "'",
    "plot_codes": "Code2",
    "data_codes": "Code3"
    }
codeinfo_code2 = {
    "codefile": "code1.csv",
    "separator": ",",
    "quote": "'",
    "plot_codes": "ISO3166-1-Alpha-2",
    "data_codes": "ISO3166-1-Alpha-3"
    }
##gdp_countries = read_csv_as_nested_dict(gdpinfo["gdpfile"],
##                                       gdpinfo["country_code"],
##                                       gdpinfo["separator"],
##                                       gdpinfo["quote"])
### problem 1 call
### a dictionary with keys of 2 letter codes and values of 3 letter codes
##plot_countries = build_country_code_converter(codeinfo)
##plot_countries = build_country_code_converter({'codefile': 'code2.csv',
##                              'quote': "'",
##                              'data_codes': 'Cd3',
##                              'plot_codes': 'Cd2',
##                              'separator': ','})
##read_csv_as_nested_dict(filename, keyfield, separator, quote)
plot_countries = build_country_code_converter(codeinfo_code1)
##print(plot_countries)

### problem 2 call
##read_csv_as_nested_dict(filename, keyfield, separator, quote):
##gdp_countries = read_csv_as_nested_dict('gdptable1.csv', 'Code',',',"'")
##reconcile_countries_by_code({'codefile': 'code2.csv', 'quote': "'", 'data_codes': 'Cd3', 'plot_codes': 'Cd2', 'separator': ','},
##                            {'C1': 'c1', 'C3': 'c3', 'C5': 'c5', 'C4': 'c4', 'C2': 'c2'},
##                            gdp_countries)
## reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)
##reconcile_countries_by_code({'codefile': 'code4.csv', 'quote': '"', 'data_codes': 'ISO3166-1-Alpha-3',
##                             'plot_codes': 'ISO3166-1-Alpha-2', 'separator': ','},
##                            {'no': 'Norway', 'pr': 'Puerto Rico', 'us': 'United States'},
##                            {'NOR': {'Country Name': 'Norway', 'Country Code': 'NOR'},
##                             'USA': {'Country Name': 'United States', 'Country Code': 'USA'},
##                             'PRI': {'Country Name': 'Puerto Rico', 'Country Code': 'PRI'}})

# problem 3 call
##p3 = build_map_dict_by_code({'quote': '"', 'gdpfile': 'gdptable1.csv', 'max_year': 2005,
##                        'separator': ',', 'country_name': 'Country Name',
##                        'min_year': 2000, 'country_code': 'Code'},
##                       {'codefile': 'code2.csv', 'quote': "'", 'data_codes': 'Cd3',
##                        'plot_codes': 'Cd2', 'separator': ','},
##                       {'C1': 'c1', 'C3': 'c3', 'C5': 'c5', 'C4': 'c4', 'C2': 'c2'},
##                            '2001')
##print(p3)
##
##print("expected:",{'C1': 0.30102999566398114, 'C3': 1.041392685158225}, {'C5', 'C4', 'C2'}, set())