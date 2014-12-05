# load necessary libraries
library(ggplot2) 
library(Matrix)
library(arules)
library(arulesSequences)
library(arulesViz)

x <- read_baskets(con = system.file("misc", "SequentialData.txt", package = "arulesSequences"), info = c("sequenceID","eventID","size"))
summary(x)
s1 <- cspade(x, parameter = list(support = 0.25), control = list(verbose = TRUE))
summary(s1)
