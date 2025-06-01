program StringTest;
var
    len: integer;
    name: string;
    greeting: string;
begin
    name := 'Pascal';
    greeting := 'Hello, ';
    
    writeln(greeting);
    
    len := length(name);
    writeln('Length of name: ', len);
    
    writeln('First character: ', name[1]);
    writeln('Last character: ', name[len]);
end.