#!/usr/bin/env Rscript

{
    library( rjags )
    library( coda )

    {    
        if ( Sys.getenv( "RSTUDIO" ) == 1 ) 
            root = "/Volumes/ginossar/aharonn/People/Tzahi/Dec-2017.good/full/summary/NegBin/"
        else
            root = "/home/labs/ginossar/aharonn/People/Tzahi/Dec-2017.good/full/summary/NegBin/"
    }
    setwd( root )
}

{
    if ( Sys.getenv( "RSTUDIO" ) == 1 ) 
    {   
        #gene = "Hnrnpab"
        #gene = "Npc2"
        #gene = "Cox8a"
        gene = "Bsg"
    }   
    else
    {   
        args = commandArgs( TRUE )
        gene = as.character( args[ 1 ]  )
    }    
}

{
    trim_5p = 6
    x.orig = my_read_table( paste0( "inps/", gene, ".csv" ) )[ , 2 ]
    x = x.orig[ ( trim_5p + 1 ) : length( x.orig ) ]
    nof_aa = trunc( length( x ) / 3 )
    x = x[ 1 : ( 3 * nof_aa ) ]
    
    x_l = list()
    for ( frame in 1 : 3 )
        x_l[[ frame ]] = x[ seq( frame, length( x ), 3 ) ]
}

{
    load( paste0( "outs/3.2/rdata/", gene, ".rdata" ) )

    df_sim = as.data.frame( mod_csim )
}

{
    mx = c()
    #for ( sim in 1 : 1000 )
    for ( sim in 1 : nrow( df_sim ) )
    {
        mu = as.numeric( df_sim[ sim, 1 : 3 ] )
        omega = as.numeric( df_sim[ sim, 4 : 6 ] )
        size = as.numeric( df_sim[ sim, 7 : 9 ] )
        for ( frame in 1 : 3 )
        {
            nof_drop = sum( rbinom( nof_aa, 1, omega[ frame ] ) )
            max_value = max( rnbinom( nof_aa - nof_drop, mu = mu[ frame ], size = size[ frame ] ) )
            mx = c( mx, max_value )
        }
    }
    mx_l = list()
    for ( frame in 1 : 3 )
        mx_l[[ frame ]] = mx[ seq( frame, length( mx ), 3 ) ]
}

{
    res = data.frame( matrix( NA, 6, 4 ) )
    names( res ) = c( "frame1", "frame2", "frame3", "nof_aa" )
    row.names( res ) = c( "max_pos", "max_val", "max_pval", "max_codon_pos", "max_codon_val", "max_codon_pval" )

    res[ 1, 4 ] = nof_aa
    for ( frame in 1 : 3 )
    {
        res[ "max_pos", frame ] = as.integer( which.max( x_l[[ frame ]] ) )
        res[ "max_val", frame ] = max( x_l[[ frame ]] )
        res[ "max_pval", frame ] = mean( mx_l[[ frame ]] >= res[ "max_val", frame ] )
    }
    
    max_codon = which.max( x_l[[ 1 ]] + x_l[[ 2 ]] + x_l[[ 3 ]] )
    for ( frame in 1 : 3 )
    {
        res[ "max_codon_pos", frame ] = max_codon
        res[ "max_codon_val", frame ] = x_l[[ frame ]][ max_codon ]
        res[ "max_codon_pval", frame ] = mean( mx_l[[ frame ]] >= res[ "max_codon_val", frame ] )
    }
    
    write.table( remove_row_names( res, "value" ), paste0( "./outs/3.2/pvals/", gene, ".csv" ), sep = "\t", row.names = F, quote = F )
}