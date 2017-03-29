import pandas as pd
import numpy as np

def main():
    district, districtGeometry, districtType, districtRatings, districtAEA, districtDistinctions, \
        districtReference, districtECHS, districtStaffStudents, districtWealth = readDistrictFiles()
    district = combineDistrictFiles(district, districtGeometry, districtType, districtRatings, districtAEA,
                                    districtDistinctions, districtReference, districtECHS, districtStaffStudents, districtWealth)

def readDistrictFiles(): 
    #read in csv files
    district = pd.read_csv('tea directory districts.csv', usecols= {0,1,2,3,4}, index_col = 0)
    districtGeometry = pd.read_csv('district_geometry.csv', usecols={'DISTRICT_N','Area'}, index_col = 'DISTRICT_N')
    #districtGeometry['DISTRICT_N']=fixZeros(list(districtGeometry['DISTRICT_N']))
    districtType = pd.read_csv('district type.csv', usecols = {1,2,3}, index_col = 'District')
    districtRatings = pd.read_csv('district ratings.csv', index_col = 'District_Number')   
    districtAEA = pd.read_csv('aea districts.csv', usecols = {1}, index_col = 'District Number')
    
    #read in xlsx files
    districtDistinctions = pd.read_excel('district_distinctions.xlsx', sheetname=0, index_col = 'DISTRICT')
    districtReference = pd.read_excel('district_reference.xlsx', sheetname=0, index_col = 'DISTRICT')
    districtStaffStudents = pd.read_excel('TAPR DISTPROF.xlsx', sheetname=0, index_col = 'DISTRICT',
                                          na_values = ['.',-1,-2,-3],
                                          parse_cols = [0,47,89,90,91,92,93,94,95,96,97,99,100,
                                                        101,102,104,123,132,150,171,172,173,247,248,253,257])
    districtECHS = pd.read_excel('Early College High Schools 15-16 list.xlsx', sheetname=0)

    #read in xls files
    districtWealth = pd.read_excel('Wealth per WADA 2016.xls', sheetname=0, index_col = 'DISTRICT')
    #get unique values from campus ECHS list as new object
    #wasn't sure if there was much benefit to having a one column data frame or a series, did frame
    districtECHS = pd.DataFrame({'DISTRICT_N':districtECHS.DistrictNumber.unique(), 'ECHS_FLAG':'Y'}) 
    
    #add missing index
    districtECHS.set_index('DISTRICT_N', inplace = True)

    #add flags
    districtAEA['AEA_FLAG'] = 'Y'
    districtDistinctions['DISTINCTION_FLAG'] = np.where(districtDistinctions['DAD_POST']=='1','Y','N')
    
    #remove extra columns
    districtRatings.drop(districtRatings.columns[[0,2,3]], axis=1, inplace=True)
    districtReference = districtReference[['DFLCHART','DI1_MET','DI1','DI2_MET','DI2','DI3_MET',
                                           'DI3','DI4_MET','DI4']]
    districtDistinctions = districtDistinctions[['DISTINCTION_FLAG']]
    
    #rename index columns to standard name
    district = district.rename(columns = {'DISTRICT_NUMBER':'DISTRICT_N'})
    districtGeometry = districtGeometry.rename(columns = {'DISTRICT_N':'DISTRICT_N'})   
    districtType = districtType.rename(columns = {'District':'DISTRICT_N'})
    districtRatings = districtRatings.rename(columns = {'District_Number':'DISTRICT_N'})  
    districtDistinctions = districtDistinctions.rename(columns = {'DISTRICT':'DISTRICT_N'})
    districtReference = districtReference.rename(columns = {'DISTRICT':'DISTRICT_N'})
    districtStaffStudents = districtStaffStudents.rename(columns = {'DISTRICT':'DISTRICT_N'})
    districtWealth = districtWealth.rename(columns = {'DISTRICT':'DISTRICT_N'})
    
    #rename other columns
    districtType = districtType.rename(columns = {'Description':'Type_Description'})
    districtReference = districtReference.rename(columns = {'DFLCHART':'CHARTER_OPERATOR'})
    districtStaffStudents = districtStaffStudents.rename(columns =
                                                         {'DPETALLC':'2016_ENROLLMENT','DPEMALLP':'2015_MOBILITY_PCT',
                                                          'DPETWHIP':'2016_WHITE_PCT','DPETBLAP':'2016_AFRAM_PCT',
                                                          'DPETHISP':'2016_HISP_PCT','DPETINDP':'2016_AMIND_PCT',
                                                          'DPETASIP':'2016_ASIAN_PCT','DPETPCIP':'2016_PACIF_PCT',
                                                          'DPETTWOP':'2016_TWO_OR_MORE_PCT',
                                                          'DPETECOP':'2016_ECODIS_PCT','DPETRSKP':'2016_AT_RISK_PCT',
                                                          'DPETLEPP':'2016_LEP_PCT','DPETSPEP':'2016_SPED_PCT',
                                                          'DPETVOCP':'2016_CTE_PCT','DPETGIFP':'2016_GT_PCT',
                                                          'DPSTTOFC':'2016_TEACHER_TOTAL_FTE',
                                                          'DPST00FC':'2016_TEACHER_BEGINNING_FTE',
                                                          'DPSATOFC':'2016_ALL_STAFF_FTE',
                                                          'DPSTURNR':'2016_TEACHER_TURNOVER_RATIO',
                                                          'DPSTTENA':'2016_TEACHER_TENURE_AVERAGE',
                                                          'DPSTEXPA':'2016_TEACHER_EXPERIENCE_AVERAGE',
                                                          'DPSTKIDR':'2016_TEACHER_STUDENT_RATIO',
                                                          'DPFEIERP':'2015_INSTRUCTIONAL_EXPENDITURES_RATIO',
                                                          'DPST00SA':'2016_TEACHER_BEGINNING_SALARY_AVERAGE',
                                                          'DPSTTOSA':'2016_TEACHER_TOTAL_SALARY_AVERAGE'})
    districtWealth = districtWealth.rename(columns = 
                                                        {'School Year 2015-2016 WADA':'2016_WADA',
                                                         'Tax Year 2014 Property Values':'2014_PropVal',
                                                         'School Year 2015-2016 Wealth per WADA':'2016_Wealth_per_WADA'})

    return district, districtGeometry, districtType, districtRatings, districtAEA, \
        districtDistinctions, districtReference, districtECHS, districtStaffStudents, districtWealth
    
def combineDistrictFiles(district, districtGeometry, districtType, districtRatings, districtAEA,
                                    districtDistinctions, districtReference, districtECHS, districtStaffStudents,districtWealth):
    district = district.join(districtReference,how='left')
    district = district.join(districtGeometry,how='left')
    district = district.join(districtType,how='left')
    district = district.join(districtAEA,how='left')
    district = district.join(districtECHS,how='left')
    district = district.join(districtRatings,how='left')
    district = district.join(districtDistinctions,how='left')
    district = district.join(districtStaffStudents,how='left')
    district = district.join(districtWealth,how='left')
    
    #convert all column names to upper case for cleanliness
    district.columns = district.columns.str.upper()
    #print(district)
    district.to_csv('district_combined.csv',sep=',')
    
    
#def fixZeros(str):
#    #pass a list of numbers formatted as string and fill in the missing leading zeros
#    maxlen = max(len(i) for i in str)
#    for i in range(len(str)):
#        if len(str[i]) < maxlen:
#            str[i] = "0"*(maxlen - len(str[i]))+str[i]
#    return str
    
main()
