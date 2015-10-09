package aan;

use strict;
use DBI;
use DBD::mysql;
use lib "/home/clairlib-dev/lib";
#use aaninc;
use Shell;

our $CURYEAR = '2011';
our @YEARS = ('2006', '2007', '2008','2009', '2010', '2011');
our @PUBLICATION_YEAR = ('1965','1966','1967','1968','1969','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010', '2011');
our @NET_TYPES = ('full-paper-citation','author-citation','author-collaboration');


sub buildmeta {
	my $metafile = shift;	
	open(IN, $metafile) || die("Metadata Error\n");
	chomp (my @metadata = <IN>);
	close IN;
	if ($metadata[$#metadata] ne "") {
		push (@metadata, "");
	}

	my %meta = ();
	my $id = "";
	my $title = "";
	my $author = "";
	my $year = "";
	my $venue = "";
	foreach my $m (@metadata) {
		$m =~ s/ +$//;
		if ($m =~ m/^id = /) {
#print "extracting id:$m\n";
			$id = $m;
			$id =~ s/^id = {//;
			$id =~ s/}//;
#print "id: $id\n";
		}
		elsif ($m =~ m/^author = /) {
			$author = $m;
			$author =~ s/^author = {//;
			$author =~ s/}//;
			$author =~ s/"//g;
#print "author: $m\n";
		}
		elsif ($m =~ m/^title = /) {
			$title = $m;
			$title =~ s/^title = {//;
			$title =~ s/}//;
			$title =~ s/,//g;
			$title =~ s/"//g;
		}
		elsif ($m =~ m/^year = /) {
			$year = $m;
			$year =~ s/^year = {//;
			$year =~ s/}//;
			$year =~ s/,//g;
			$year =~ s/"//g;
		}
		elsif ($m =~ m/^venue = /) {
			$venue = $m;
			$venue =~ s/^venue = {//;
			$venue =~ s/}//;
			$venue =~ s/,//g;
			$venue =~ s/"//g;
		}
		else {
			my $string = $author . " ::: " . $title . " ::: " . $year . " ::: " . $venue;
			$meta{$id} = $string;
			$author = "";
			$title = "";
			$year = "";
			$venue = "";
			$id = "";
		}
	}
	return %meta;
}

sub select_year {
		
		my ($id, $to_year, $self);
		$self = 0;
		$id = $_[0];
		my @paper_id =  split(//,"$id");
		$to_year = $_[1];
		my $paper_year;
		if($paper_id[1] == '0')
		{
				$paper_year = "20" . $paper_id[1] . $paper_id[2];
		}
		else
		{
				$paper_year = "19" . $paper_id[1] . $paper_id[2];
		}
		if($paper_year <= $to_year)
		{
				$self = 1;
		}
		$self;
}

sub find_start_delimiter {
		
	my $str = shift;	
	my $start_auth_name = shift;
	my $col_index = index($str,"; ", $start_auth_name);
	my $length = length($str);
	if($col_index == -1)
	{
			return -1;
	}
	else
	{
			my $prev_char = substr($str,$col_index-1,1);
			if($prev_char eq ';')
			{
					my $ret_index = index($str,"; ", $col_index+1);
					return $ret_index;
			}
			else
			{
					return $col_index;
			}
	}

}

sub make_well_formed {

		my $author_string = shift;
		my $amp_index = -1;
		$amp_index = index($author_string,"&",0);
		while($amp_index != -1)
		{
				my $col_index = index($author_string,";",$amp_index);
				if($col_index == -1)
				{
						return 0;
				}
				$amp_index = index($author_string,"&", $col_index+1);
		}
		return 1;
}

sub extract_authors {
	my $auth_string = shift;
	my @authors = ();
	my $len = length($auth_string);
	my $auth_start = 0;
	my $delim_start = find_start_delimiter($auth_string,$auth_start);
	while($delim_start != -1)
	{
			my $author = substr($auth_string,$auth_start,$delim_start-$auth_start);
			my $is_wellformed = make_well_formed($author);
			if($is_wellformed == 0)
			{
					$author = $author.";";
			}
			if($author ne "")
			{
				$author =~ s/;;/;/g;
				push(@authors,$author);
			}
			$auth_start = $delim_start+2;
			$delim_start = find_start_delimiter($auth_string,$auth_start);
	}

	my $last_author = substr($auth_string,$auth_start,$len-$auth_start);
	my $is_wellformed = make_well_formed($last_author);
	if($is_wellformed == 0)
	{
		$last_author = $last_author.";";
	}
	if($last_author ne "")
	{
		$last_author =~ s/;;/;/g;
		push(@authors,$last_author);
	}
	return \@authors;
}

