program StringTest;
var
    name: string;
    greeting: string;
    len: integer;
begin
    name := 'Pascal';
    greeting := 'Hello, ';
    
    writeln(greeting);
    
    len := length(name);
    writeln('Length of name: ', len);
    
    writeln('First character: ', name[1]);
    writeln('Last character: ', name[len]);
end.