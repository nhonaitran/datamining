# load necessary libraries
library(ggplot2) 
library(arules)
library(arulesViz)
##########################################
## Unique page hits excluding frontpage
##########################################
# load page hit data
system.time(transactions <- read.transactions("assets/unique_pagehits_exclude_frontpage.csv", format="basket", sep=","))
itemFrequency(transactions)
# plot frequency of each category
itemFrequencyPlot(transactions, support=0.001)

summary(transactions)

system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.1, minlen=2)))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.1, target="maximally frequent itemsets")))

# find rules that have minimum support and confidence = 1% and 70%
system.time(rules <- apriori(transactions, parameter = list(supp=0.001, conf=0.50, minlen=2)))

# find 2-itemset rules that have minimum support and confidence being 1\% and 35\%
system.time(rules <- apriori(transactions, parameter = list(supp=0.02, conf=0.35, minlen=2, maxlen=2)))

system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01), appearance = list(lhs = c("frontpage","business","local","news","on-air","sports","tech"), default="lhs") ))

# find rules that have the following conditions
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("bbs"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("business"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("health"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("living"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("local"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("misc"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("msn-news"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("msn-sports"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("news"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("on-air"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("opinion"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("sports"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("summary"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("tech"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("travel"), default="rhs")))
system.time(rules <- apriori(transactions, parameter = list(supp=0.01, conf=0.01, minlen=2), appearance = list(lhs = c("weather"), default="rhs")))
inspect(rules)
summary(rules)

plot(rules, measure="support", shading="lift")
plot(rules, measure=c("support","lift"), shading="confidence")
plot(rules, shading="order", control=list(main="Two-key plot"))

# interactive plot
sel <- plot(rules, measure=c("support","lift"), shading="confidence", interactive=TRUE)

plot(rules, method="matrix", measure="lift")
plot(rules, method="matrix", measure="lift", control=list(reorder=TRUE))
plot(rules, method="matrix", measure=c("lift","confidence"))
plot(rules, method="matrix", measure=c("lift","confidence"), control=list(reorder=TRUE))
plot(rules, method="grouped")
plot(rules, method="grouped", control=list(k=50))

sorted <- sort(rules, by="support")
plot(sorted, method="graph", control=list(type="items"))

sortedByLift <- sort(rules, by="lift")
plot(sorted, method="graph", control=list(type="items"))

plot(sorted, method="paracoord")
plot(sorted, method="paracoord", control=list(reorder=TRUE))

plot(rules, method="matrix3D", measure="lift")
plot(rules, method="matrix3D", measure="lift", control=list(reorder=TRUE))