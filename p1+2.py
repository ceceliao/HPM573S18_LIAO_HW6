import numpy as np
import scr.FigureSupport as figureLibrary
import scr.StatisticalClasses as Stat

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250

    def get_loss(self,n_of_flips):
        count_loss=0
        for i in range(n_of_flips):
            if 100*self._countWins-250 < 0:
                count_loss+=1
        return count_loss


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._loss=[]
        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())
            self._loss.append(game.get_loss(20)/len(self._gameRewards))

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)


    def get_ave_probability_loss(self):
        """ returns the probability of a loss """
        count_loss = 0
        for value in self._gameRewards:
            if value < 0:
                count_loss += 1
        return sum(self._loss) / len(self._gameRewards)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards

    def get_loss_list(self):
        return self._loss

    def simulation(self):
        return CohortOutcomes(self)


class CohortOutcomes:
    def __init__(self,simulated_cohort):
        self._simulatedCohort = simulated_cohort

        self._sumStat_rewards = \
            Stat.SummaryStat('total rewards', self._simulatedCohort.get_reward_list())
        self._sumStat_loss = \
            Stat.SummaryStat('The probability of loss', self._simulatedCohort.get_loss_list())

    def get_CI_expected_rewards(self,alpha):
        return self._sumStat_rewards.get_t_CI(alpha)

    def get_CI_probability_loss(self,alpha):
        return self._sumStat_loss.get_t_CI(alpha)


trial = SetOfGames(prob_head=0.5, n_games=1000)
cohortOutcome=trial.simulation()
print("The 95% t-based CI for the expected reward:", cohortOutcome.get_CI_expected_rewards(0.05))
#Interpretation: If the same study is repeated for many times, 95% of the CIs created from the each simulation (-31.79, -20.01) will cover the expected reward true mean.

print("The 95% t-based CI for the expected probability of loss:", cohortOutcome.get_CI_probability_loss(0.05))
#Interpretation: If the same study is repeated for many times, 95% of the CIs created from the each simulation (0.063, 0.119) will cover the probability of loss true mean.




