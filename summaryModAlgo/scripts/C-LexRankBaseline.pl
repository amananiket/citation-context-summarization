#! /usr/local/bin/perl

use Clair::Utils::Stem;
use Clair::Document;
use strict;
use FindBin;
use Clair::Cluster;
use Clair::Network;
use Clair::Network::CFNetwork;
use Clair::Network::Centrality::LexRank;
use Clair::Network::Centrality::Betweenness;
use Set::Scalar;


my $limit = shift;
my $file = shift;
my $cutoff = 0.0;

my $name = &getFileName($file);

my %sents = ();
my %origSents =();
my $id = 0;
my @files = ();
push(@files, $file);

for my $file (@files){    
    open IN, "$file";    
    while(<IN>){
	chomp $_;
	my $orig = $_;
	my $l = $_;
	$l = lc($l);
	$l =~ s/\([^\)]+\)/ /g;
	$l =~ s/\[[^\]]+\]/ /g;
	$l =~ s/\s+/ /g;
	++$id;
	$sents{$id} =  $l;
	$origSents{$id} = $orig;
    }
}

my $totalsents = keys %sents;
if($totalsents <= 3)
{
    my $summary = "";
    for my $i (keys %sents)
    {
	$summary = $summary . $origSents{$i}."\n";
    }
    open OUT, ">../modOutput/".$name."-C-LR.txt";
    print OUT "$summary";
    print $summary;
    exit;
}


my $cluster = Clair::Cluster->new();
for my $id (keys %sents){
    my $sent = $sents{$id};
    my $doc = new Clair::Document(type => 'text', string => $sent, id => $id);
    $cluster->insert($id, $doc);
}

$cluster->stem_all_documents();	
my %sims = $cluster->compute_cosine_matrix();

my $self = $cluster;
my %documents = %{ $self->{documents} };

my $stemmedSents = "";

#foreach my $doc (values %documents) {
#	$stemmedSents = $stemmedSents.$doc->get_text()."\n";	
#}

for my $s (keys %sents){
	$stemmedSents = $stemmedSents.$s. "\t".$sents{$s}."\n";
}


# open OUT, ">outputs/tempSents.txt";
# print OUT "$stemmedSents";

# open OUTP, ">outputs/perlSims.txt";

# for my $s1 (keys %sents){
#     for my $s2 (keys %sents){
# 	print OUTP $s1."\t".$s2."\t";
	
# 	my $sim = $sims{$s1}{$s2};
# 	print OUTP $sim."\n";
#     }
# }

# for my $s (keys %sents){
# 	print OUTP $s. "\t".$sents{$s}."\n";
# }


my %nodes = ();
my $cfnw = Clair::Network::CFNetwork->new(name => $name); 

for my $s1 (keys %sents){
    for my $s2 (keys %sents){
	my $sim = $sims{$s1}{$s2};
	if($sim >= $cutoff){
	    $cfnw->add_weighted_edge($s1, $s2, $sim);
	}
    }
}

my $subcfnw = $cfnw->getConnectedComponent(1);
$subcfnw->communityFind(dirname => "../temp", skip_connection_test => 1);

my %communities = ();
my %comsize = ();
if(-e "../temp/".$name.".bestComm")
{
    open IN, "../temp/".$name.".bestComm";
    while(<IN>){
	chomp $_;
	my @arr = split(/ /, $_);
	my $id = $arr[0];
	my $comm = $arr[1];
	if(! exists $comsize{$comm}){
	    $comsize{$comm} = 1;
	}else{
	    $comsize{$comm} = $comsize{$comm} +1 ;
	}
	$communities{$comm}{$id} = 1; 
    }
}else
{
    for my $i(keys %sents)
    {
	my $comm = 1;
	if(! exists $comsize{$comm}){
	    $comsize{$comm} = 1;
	}else{
	    $comsize{$comm} = $comsize{$comm} +1 ;
	}
	$communities{$comm}{$i} = 1; 
    }
}

my %commLexRank = ();

for my $com (keys %communities){
    my $comcluster = Clair::Cluster->new();
    for my $id (keys %{$communities{$com}}){
	my $sent = $sents{$id};
	my $doc = new Clair::Document(type => 'text', string => $sent, id => $id);
	$comcluster->insert($id, $doc);
    }
    my %scores = $comcluster->compute_lexrank(cutoff=>0.1);
    for my $t (sort {$scores{$b}<=> $scores{$a}} keys %scores){
	$commLexRank{$com}{$t} = $scores{$t};
    }
}

my %rankedSents = ();
my $i = 0;
for my $comm (sort {$comsize{$b} <=> $comsize{$a}} keys %comsize){
    ++$i;
    my $j = 0;
    for my $id (sort {$commLexRank{$comm}{$b} <=> $commLexRank{$comm}{$a}} keys %{$commLexRank{$comm}}){	
	++$j;
	my $sent = $origSents{$id};
	$rankedSents{$j}{$i} = $sent; 
    }
}

my $numorigSents = keys %sents;
if($numorigSents < $limit)
{
    $limit = $numorigSents;
}

my $summary = "";
my $count = 0;
my $words = 0;

for my $jj (sort {$a<=>$b} keys %rankedSents)
{
    for my $ii (sort {$rankedSents{$a}<=>$rankedSents{$b}} keys %{$rankedSents{$jj}})
    {
	++$count;    
	$summary = $summary.$rankedSents{$jj}{$ii}."\n";

      my @wordsArray = split(/ /, $rankedSents{$jj}{$ii});
      $words += scalar @wordsArray;
      print $words."\n";
    
      if ($words > 100) {
     	 last;
      }
    
    }
   
	 if ($words > 100) {
     	 last;
      }
 
    
}

open OUT, ">../modOutput/".$name."-C-LR.txt";
print OUT "$summary";
print "$summary";
close OUT;


sub getFileName{
    my $file = shift;
    my @temp = split(/\//, $file);
    my $name = $temp[$#temp];
    @temp = split(/\./, $name);
    $name = $temp[0];
    return $name;
}

sub shouldContinue{
    my ($summary, $limit) = @_;
    my $sumlen = &getLength($summary);
    if($sumlen < $limit){
	return 1;
    }
    else{
	return 0;
    }
}


sub getLength{
    my $summary = shift;    
    my @list = split(/\s/, $summary);
    my $len = $#list+1;    
    return $len;
}

sub addSent{
    my ($summary, $sent, $limit) = @_;
    $sent =~ s/\s+$//g;
    $sent =~ s/^\s+//g;
    my $sumlen = &getLength($summary);   
    my $budget = $limit - $sumlen;
    my $sentlen = &getLength($sent);
    if($budget > $sentlen){
	$summary .= "$sent\n";
    }else{
	my @temp = split(/ /, $sent);
	for (my $i=0; $i< $budget; ++$i){
	    $summary = $summary.$temp[$i]." ";
	}
	chop $summary;
	$summary .= "\n";
    }
    $sumlen = &getLength($summary);
    return $summary;
}
