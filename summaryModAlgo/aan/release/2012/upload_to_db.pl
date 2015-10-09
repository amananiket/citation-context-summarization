use strict;

use DBI;

my $dsn = 'DBI:mysql:database=aan:localhost';

my $user = 'clair'; 
my $pass = 'cfhoCPkr';

# now connect and get a database handle

my $author_ids = shift;
my $author_hindex = shift;

open IDS, "$author_ids";
open IDX, "$author_hindex";

my $dbh = DBI->connect($dsn, $user, $pass)  or die "Can't connect to the DB: $DBI::errstr\n";

my %ids = ();

while(<IDS>){
	chomp;
	my @cols = split /\t/;
	$ids{$cols[1]} = $cols[0];
}

my $query = "INSERT INTO author_info(id, hindex) VALUES ";

while(<IDX>) {
	chomp;
	my @cols = split /\t/;
	my $id = $ids{$cols[1]};
	my $hindex = $cols[0];
	$query .= "('$id', '$hindex'), ";
}

$query =~ s/,\s+$//;

$query .= " ON DUPLICATE KEY UPDATE hindex = VALUES(hindex);";

my $sth = $dbh->prepare($query);
$sth->execute;
