program ArrayTest;
var
numbers: array[1..5] of integer;
grades: array[1..3] of integer;
i: integer;
average: real;
begin

numbers[1] := 10;
numbers[2] := 20;
numbers[3] := 30;
numbers[4] := 40;
numbers[5] := 50;

for i := 1 to 5 do writeln('Element ', i, ': ', numbers[i]);


grades[1] := 85;
grades[2] := 92;
grades[3] := 78;

average := 0;
for i := 1 to 3 do
    average := average + grades[i];
average := average / 3;

writeln('Average grade: ', average);
end.