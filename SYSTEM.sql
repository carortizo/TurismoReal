create user c##turismo identified by oracle;

grant connect, resource to c##turismo;

alter user c##turismo default tablespace users quota unlimited on users;