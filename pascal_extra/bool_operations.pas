program BooleanTest;
var
    flag1, flag2: boolean;
    result: boolean;
    num: integer;
begin
    flag1 := true;
    flag2 := false;
    
    result := flag1 and flag2;
    writeln('true AND false = ', result);
    
    result := flag1 or flag2;
    writeln('true OR false = ', result);
    
    result := not flag1;
    writeln('NOT true = ', result);
    
    num := 7;
    result := (num > 5) and (num < 10);
    writeln('7 is between 5 and 10: ', result);
end.