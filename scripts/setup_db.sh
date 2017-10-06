sudo -u postgres bash -c "psql -c \"CREATE USER hotohete WITH PASSWORD 'testtest';\""
sudo -u postgres bash -c "psql -c \"ALTER USER hotohete CREATEDB;\""
sudo -u postgres bash -c "psql -c \"CREATE DATABASE hotohete;\""
sudo -u postgres bash -c "psql -c \"ALTER DATABASE hotohete OWNER TO hotohete;\""
