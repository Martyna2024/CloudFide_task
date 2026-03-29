import re
import pandas
import operator

operators = {
    '+': operator.add,
    '*': operator.mul,
    '-': operator.sub
}

def add_virtual_column(df: pandas.DataFrame, role: str, new_column: str) -> pandas.DataFrame:
    
    # I'm veryfing  if input new column name is correct
    if re.search(r'[^a-zA-Z_]', new_column):
        return(pandas.DataFrame([]))

    # I'm veryfing of the input data type is correct
    if not isinstance(df, pandas.DataFrame) or not isinstance(role, str) or not isinstance(new_column, str):
        return(pandas.DataFrame([]))
    
    # Transforming input role from str into list of str
    split_text = re.findall(r'\w+|[+\-*]', role)
        
    # Checking if column names in input role are correct
    for index in range(0, len(split_text), 2):
        if split_text[index] not in df.columns:
            return(pandas.DataFrame([]))

    # Converting into a list of columns as pandas df and operators as str for easier calculations
    convert_split_text = [df[column] if column in df.columns else column for column in split_text]
             
    # Checking whether input columns in role are float or int
    for index in range(0, len(split_text), 2):
        if convert_split_text[index].dtype not in ['int64', 'int32', 'float64', 'float32']:
            return(pandas.DataFrame([]))
        
    # Taking into consideration calculation priotity so the multiplication is always calculated 1st (task description only mentiones substraction, addition and multiplication so that is all that was included) 
    index = 0
    while index < len(convert_split_text):
        if isinstance(convert_split_text[index], str) and convert_split_text[index] == '*':
            st_column = convert_split_text[index - 1]
            nd_column = convert_split_text[index + 1]

            calculation = st_column * nd_column

            # Deleting columns, adding the value of multiplication to the list
            convert_split_text[index] = calculation
            del convert_split_text[index+1]
            del convert_split_text[index-1]

            # Moving index back to recheck
            index = index - 1
                
        else:
            #Moving index forward to check the next element
            index = index + 1
        
                                              
    # Calculation of the final output (only addition and substraction)
    calculation = convert_split_text[0]
    for index in range(1, len(convert_split_text), 2):
        operator = convert_split_text[index]
        nd_column = convert_split_text[index + 1]
        calculation = operators[operator](calculation, nd_column)

    # Adding it to the dataframe
    df[new_column] = calculation
    return(df)

