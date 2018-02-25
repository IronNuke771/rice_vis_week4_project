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
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            row_key = row[keyfield]
            return_dict[row_key] = row
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
    cc_dict = read_csv_as_nested_dict(codeinfo["codefile"],
                                      codeinfo["plot_codes"],
                                      codeinfo["separator"],
                                      codeinfo["quote"])
    for key,val in cc_dict.items():
        code_convert_dict[key] = val[codeinfo["data_codes"]]
##    print("------BUILD COUNTRY CODE CONVERT-------")
##    print(code_convert_dict)
##    print("")
    return code_convert_dict

def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
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
    net_key_dict = {}
    recon2_dict = {}
    recon2_set = set()
    code_convert_dict = build_country_code_converter(codeinfo)
    
##    print("plot_countries",plot_countries)
##    print("code convert dict",code_convert_dict)
##    print("GDP table")
##    for key,val in gdp_countries.items():
##        print(key,val)
##    print("")

    # Get the matched items from the plot dict and the convert dict
    for plot_key in plot_countries.keys():
        for cc_key,cc_val in code_convert_dict.items():
            if plot_key.upper() == cc_key.upper():
                net_key_dict[plot_key]=cc_val
                
##    print('net_key_dict',net_key_dict)
    
    # Populate the return dict
    for npk_key,npk_value in net_key_dict.items():
        for gdp_key in gdp_countries.keys():
##            print(npk_value,gdp_key)
            if npk_value.upper() == gdp_key.upper():
##                print(npk_value,gdp_key)
                recon2_dict[npk_key] = gdp_key

    # Populate the return set
    for nkd_key,nkd_val in net_key_dict.items():
        if nkd_val.upper() not in [gdp_val.upper() for gdp_val in gdp_countries.keys()]:
            recon2_set.add(nkd_key)
    
##    print("------RECONCILE COUNTRY BY CODE------")
##    print("plot / gdp matched",recon2_dict)
##    print("unmatched countries",recon2_set)
##    print("-----------")
##    print("")
    return recon2_dict, recon2_set


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
    return_dict = {}
    return_set1 = set(plot_countries)
    return_set2 = set()
    gdp_countries = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                       gdpinfo["country_code"],
                                       gdpinfo["separator"],
                                       gdpinfo["quote"])
    net_plot_dict = reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)[0]
##    no_gdp_code = reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)[1]
##    print("plot countries",plot_countries)
##    print("net_plot_dict",net_plot_dict)
##    print("no_gdp_code",no_gdp_code)
##    print("gdp dict", gdp_countries)
    
    # Populate the return dictionary
    for pygal_code,gdp_code in net_plot_dict.items():
        ann_gdp = gdp_countries[gdp_code][year]
        if ann_gdp.isnumeric and len(ann_gdp):
            log_ann_gdp = math.log(float(ann_gdp),10)
            return_dict[pygal_code] = log_ann_gdp
            return_set1.remove(pygal_code)
        else:
            return_set2.add(pygal_code)
            return_set1.remove(pygal_code)

##    print("------BUILD MAP DICT BY CODE------")
##    print(return_dict)
##    print(return_set1)
##    print(return_set2)
    return return_dict, return_set1, return_set2

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
    gdp_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                       gdpinfo["country_code"],
                                       gdpinfo["separator"],
                                       gdpinfo["quote"])
    plot_countries = build_country_code_converter(codeinfo)
    rec_countries = reconcile_countries_by_code(codeinfo, plot_countries, gdp_dict)
    map_tuple = build_map_dict_by_code(gdpinfo, codeinfo, rec_countries[0], year)
    
    plot_gdp = {}
    for key,val in map_tuple[0].items():
        plot_gdp[key.lower()] = val
##    print(plot_gdp)
##    print(map_tuple[2])
    no_wb_data = set([x.lower() for x in list(map_tuple[1])])
##    print(no_wb_data)
    no_gdp_data = set([x.lower() for x in list(map_tuple[2])])
##    print(no_gdp_data)
    # Build the map
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = 'Global GDP by Country for ' + str(year)
    worldmap_chart.add("GDP",plot_gdp)
    worldmap_chart.add("Not in WB Data",no_wb_data)
    worldmap_chart.add("no GDP data",no_gdp_data)
    worldmap_chart.render_in_browser()

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

test_render_world_map()

######################################################################
##p3 = build_map_dict_by_code({'country_code': 'Code', 'max_year': 2005, 'quote': '"',
##                        'separator': ',', 'min_year': 2000, 'country_name': 'Country Name',
##                        'gdpfile': 'gdptable1.csv'},
##                       {'quote': "'", 'separator': ',', 'data_codes': 'Cd3',
##                        'codefile': 'code2.csv', 'plot_codes': 'Cd2'},
##                       {'C3': 'c3', 'C1': 'c1', 'C5': 'c5', 'C2': 'c2', 'C4': 'c4'}, '2001')
##p3 = build_map_dict_by_code({'quote': '"', 'gdpfile': 'gdptable2.csv', 'max_year': 1958,
##                        'separator': ',', 'country_name': 'Country Name',
##                        'min_year': 1953, 'country_code': 'Code'},
##                       {'codefile': 'code2.csv', 'quote': "'",
##                        'data_codes': 'Cd1', 'plot_codes': 'Cd2', 'separator': ','},
##                       {'C1': 'c1', 'C3': 'c3', 'C5': 'c5', 'C4': 'c4', 'C2': 'c2'}, '1953')
##
##build_map_dict_by_code({'quote': "'", 'gdpfile': 'gdptable3.csv', 'max_year': 20017,
##                        'separator': ';', 'country_name': 'ID', 'min_year': 20010,
##                        'country_code': 'CC'}, {'codefile': 'code1.csv',
##                        'quote': "'", 'data_codes': 'Code3', 'plot_codes': 'Code4',
##                        'separator': ','},
##                       {'C1': 'c1', 'C3': 'c3', 'C5': 'c5', 'C4': 'c4', 'C2': 'c2'}, '20012')
##build_map_dict_by_code({'country_code': 'Code', 'max_year': 2005, 'quote': '"',
##                        'separator': ',', 'min_year': 2000, 'country_name': 'Country Name',
##                        'gdpfile': 'gdptable1.csv'}, {'quote': "'", 'separator': ',',
##                        'data_codes': 'Cd3', 'codefile': 'code2.csv', 'plot_codes': 'Cd2'},
##                       {'C3': 'c3', 'C1': 'c1', 'C5': 'c5', 'C2': 'c2', 'C4': 'c4'}, '2001')