#!/usr/bin/perl 
#script: h-index.pl
#functionality: calculates h-index on the acl anthology network

use warnings;
use aan;
use Getopt::Long;

#data input files
my $acl_file = '';
my $metafile = '';
my $to_year = 2012;
my $release = 2012;
my $nonself = 0;
my $help = 0;


my %authors = ();		#hash to hold author paper arrays
my %cites = ();			#hash to hold paper citations
my %hindex = ();		#hash to hold author h-index scores
my %titles = ();		#hash to hold paper titles

my $res = GetOptions("release:i" => \$release, 
					 "year:i" => \$to_year,
					 "nonself" => \$nonself,
					 "help" => \$help);

if($help)
{
		usage();
		exit;
}

$metafile = "../$release/acl-metadata.txt";
$acl_file = "../$release/acl.txt";


my %meta = aan::buildmeta($metafile);
##acl-metatdata example
#id = {J79-1002}
#author = {Fitzpatrick, Eileen; Sager, Naomi}
#title = {The Lexical Subclasses Of The Linguistic String Parser}
#venue = {ACL Microfiche Series 1-83, Including Computational Linguistics}
#year = {1979}

#create hash of arrays: authors->papers
#and paper titles
open ACLM, $metafile or die "Can't open metadata file $metafile: $!\n";
my $id = '';
my @auths = ();
while(<ACLM>) {
  chomp;
  if (/id.*\{(.*)\}/) {
    $id = $1;
    @auths = ();
  }elsif ($id && /author.*\{(.*)\}/) {
#@auths = split '; ', $1;
	@auths = @{aan::extract_authors($1)};
	
	  foreach my $auth (@auths) {
      unless( $authors{$auth} ) {
        $authors{$auth} = ();
      }
	  if(&aan::select_year($id,$to_year) == 1) {
	      push @{$authors{$auth}}, $id;
	  }
    }
  }
  elsif ($id && /title.*\{(.*)\}/) {
    $titles{$id} = $1;
  }  
}
close ACLM;

##test for authors hash
#foreach my $auth (sort keys %authors){
#  print "\n$auth\n";
#  foreach (@{$authors{$auth}}) {
#    print "\t$_\n";
#  }
#}

#create citation hash: paper->citations
open ACL, $acl_file or die "Can't open acl $acl_file: $!\n";
while(<ACL>) {
  chomp;
  my($out, $in) = split ' ==> ';
  if(&aan::select_year($out,$to_year) == 1 && &aan::select_year($in,$to_year) == 1) 
  {
	if(!$nonself || &isSelfCitation($out,$in) == 0)
	{
	  	$cites{$in}++;
	}
  }
}
close ACL;

##test for citation hash
#foreach my $p (sort keys %cites){
#  print "$p: $cites{$p}\n";
#}

#get h-index for selected author or each author

  foreach my $auth (sort keys %authors) {
    $hindex{$auth} = &get_h_index($auth);
  }
  
  #print out the h-indexes: h-index tab author
  foreach my $auth ( sort keys %hindex ) {
		 if($auth ne "") {
	   		 print "$hindex{$auth}\t$auth\n";
		 }
  }



##SUBS-----

sub get_h_index {

  my $auth = shift;
  my $listref = 0;
 
  #get citations for papers
  $listref = &get_cites_list($auth);
 
  my $h = 0;
  my $papernum = 0;  
  my $ncite = 0; 

  #get citations for paper at index 0
  my $paperid = $$listref[$papernum];
  $ncite = $paperid && $cites{$paperid} ? $cites{$paperid} : 0;

  while($paperid && $ncite > $papernum) {
    $h++;
    $papernum++;
    $paperid = $$listref[$papernum];
    $ncite = $paperid && $cites{$paperid} ?  $cites{$paperid} : 0;
  }

  return $h;

}   

sub get_cites_list {

  my $auth = shift;
  my @citeslist = ();
  my %tmp = ();

  #get citations for papers
  foreach my $paper (@{$authors{$auth}}) {
    if ( $cites{$paper} ) {
      $tmp{$paper} = $cites{$paper};
    }else{
      $tmp{$paper} = 0;
    }
  }

  @citeslist = sort { $tmp{$b} <=> $tmp{$a} } keys %tmp;

  return \@citeslist;
}

sub isSelfCitation {
		my ($from, $cites);
		$from = $_[0];
		$cites = $_[1];
#my %meta = $_[2];

		$self = 0;
		if(! exists($meta{$from}))
		{
			return 0;
		}
		if(! exists ($meta{$cites}))
		{
			return 0;

		}

		my $from_auths = $meta{$from};
		$from_auths =~ s/ ::: .+//;
		$from_auths =~ s/ :: /; /;
		my $cites_auths = $meta{$cites};
		$cites_auths =~ s/ ::: .+//;
		$cites_auths =~ s/ :: /; /;


		my (@fas, @cas);
		if (($from_auths ne "na") && ($cites_auths ne "na") && ($cites_auths ne "") && ($cites_auths ne "")) {
				if ($from_auths =~ m/;/) {
						@fas = split(/; /, $from_auths);
				}
				else {
						push(@fas, $from_auths);
				}
				if ($cites_auths =~ m/;/) {
						@cas = split(/; /, $cites_auths);
				}
				else {
						push(@cas, $cites_auths);
				}
				foreach my $fa (@fas) {
						foreach my $ca (@cas) {
								if($fa eq $ca)
								{
										$self = 1;
										last;
								}
						}
				}
		}
		$self;
}




sub usage
{
		print "Usage: $0 [-release=release_year] [-year=to_year] [-nonself] [-help]\n\n";
		print "\t-release=release_year\n";
		print "\t\tCan be any one of 2008, 2009, 2010 or 2011, defaults to 2011.\n";
		print "\t-year=to_year\n";
		print "\t\twhen specified, only citations which are older than the year mentioned are included. Can be any year greater than 1965, defaults to 2011.\n";
		print "\t-nonself\n";
		print "\t\twhen specified, self citations are excluded. By default self citations are NOT excluded.\n";
		print "\t-help\n";
		print "\t\tprints out the different options available\n";
}
