# load necessary libraries
library(ggplot2)  #for plotting
library(arules)

# load page hit data
transactions <- read.transactions("assets/unique_pagehits.csv", format="basket", sep=",")

# plot frequency of each category
itemFrequencyPlot(transactions, support=0.001)

# find rules that have minimum support and confidence being 1\% and 1\%
rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.75, minlen=2))

# find 2-itemset rules that have minimum support and confidence being 1\% and 35\%
rules <- apriori(transactions, parameter = list(supp=0.02, conf=0.35, minlen=2, maxlen=2))

rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01), appearance = list(lhs = c("frontpage","business","local","news","on-air","sports","tech"), default="lhs") )

# find rules that have rhs=Front page
rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01), appearance = list(lhs = c("frontpage"), default="lhs") )

inspect(rules)

#interestMeasure(rules, c("support", "chiSquare", "confidence", "cosine", "coverage", "lift"), transactions)
