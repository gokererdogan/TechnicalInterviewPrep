# 4 Jan. 2017
import numpy as np


def dag_to_fg(adj_dag, potentials):
    """
    Given adjacency matrix for directed graph and potentials for each node, form the factor graph

    Parameters:
        adj_dag: adjacency matrix of the directed graphs
        potentials: a list of numpy arrays.
            potentials[i] is the conditional distribution of node i given its parents
            parents are assumed to be sorted
            e.g., for node 2 with parents 3, 1 potentials[2] is p(2|1,3)
            We assume each variable is binary. Hence, potentials[i] is of size (2)^(parent count + 1),
            with one dimension for each variable.

    Returns:
        numpy.ndarray: adjacency matrix for the factor graph.
            Nodes 0:n are variable nodes. Nodes n:2n are factor nodes.
            There is one factor node for each variable node.
        dictionary: factor potentials containing a potential for each factor node.
            Note the variables in the factor are ordered, e.g., the conditional distribution
            p(2|1,3) becomes factor f(1,2,3)
    """
    N = adj_dag.shape[0]
    adj_fg = np.zeros((2*N, 2*N), dtype=np.bool)
    factor_potentials = {}
    for n in range(N):  # for every node, construct its factor
        # connect current node to its factor
        adj_fg[n, N+n] = 1
        adj_fg[N+n, n] = 1
        # connect the parents of node to factor
        n_parents = list(np.nonzero(adj_dag[:, n])[0])
        for p_n in n_parents:
            adj_fg[p_n, N+n] = 1
            adj_fg[N+n, p_n] = 1
        # check if potential is valid
        assert(potentials[n].shape == (2,) * (len(n_parents) + 1))
        # sort the node ids. we want the factor dimensions sorted according to node ids.
        sort_ix = list(np.argsort([n] + n_parents))
        # directed potential is for n|parents(n) where parents(n) are sorted
        # we need to reorder its dimensions so all nodes in the factor are sorted
        factor_potentials[N+n] = np.transpose(potentials[n], axes=sort_ix).copy()
    return adj_fg, factor_potentials


def is_leaf(adj, i):
    neighbor_count = np.sum(adj[i])
    assert(neighbor_count > 0)
    return neighbor_count == 1


def is_factor_node(adj_fg, i):
    # factor nodes are always after variable nodes, i.e., 0:n are variable nodes, n:2n are factor nodes.
    return i >= (adj_fg.shape[0] / 2)


def get_neighbors(adj, i):
    return list(np.nonzero(adj[i])[0])


def message_passing(adj_fg, potentials, evidence={}):
    """
    Message passing algorithm.

    Parameters:
        adj_fg: adjacency matrix of the factor graph
        potentials: a dictionary of factor potentials

        dag_to_fg algorithm converts directed graph and conditional probability distributions
        to factor graph and associated factor potentials.

    Results:
        marginals: A list of marginal distributions for each node
        messages: A dictionary of messages passed.
            key (i, j) contains the message from node i to j
    """
    N = adj_fg.shape[0]
    assert(N%2 == 0)  # one factor for each variable node
    messages = {}
    # i, j is True if message i->j is computed
    is_computed = np.zeros_like(adj_fg, dtype=np.bool)

    while True:  # loop until all messages are computed
        all_computed = True
        for from_node in range(N):  # loop over each node in the factor graph
            neighbors = get_neighbors(adj_fg, from_node)
            # try to calculate the message from node to its neighbors
            for to_node in neighbors:
                if not is_computed[from_node, to_node]:
                    # can we compute this message? are messages from other neighbors computed?
                    # we need messages from all neighbors except to_node
                    needed_neighbors = [e for e in neighbors if e != to_node]
                    if np.all(is_computed[needed_neighbors, from_node]):
                        # we have all necessary messages.
                        # compute the message
                        if is_factor_node(adj_fg, from_node):  # factor to variable message
                            # initialize to factor potential
                            message = potentials[from_node].copy()

                            # multiply by each incoming message from variable to factor
                            factor_variables = sorted(neighbors)
                            for i, v in enumerate(factor_variables):
                                if v != to_node:
                                    # make sure that we are multiplying the potential correctly
                                    # we need to broadcast the message from v along all dimensions except its
                                    # own dimension
                                    # since the variables in a factor are ordered, v is in dimension i.
                                    broadcast_shape = np.ones(len(factor_variables))
                                    broadcast_shape[i] = -1
                                    message *= np.reshape(messages[(v, from_node)], broadcast_shape)

                            # marginalize over all except the target variable
                            if len(factor_variables) > 1:
                                # we need to sum over all variables except to_node
                                sum_over = range(len(factor_variables))
                                del sum_over[factor_variables.index(to_node)]
                                message = np.sum(message, axis=tuple(sum_over))

                            if to_node in evidence:
                                assert(evidence[to_node] in [0, 1])
                                zero_state = 0 if evidence[to_node] == 1 else 1
                                message[zero_state] = 0.0
                        else:
                            # variable to factor message
                            message = np.ones(2)
                            # multiply messages from all neighbors except to_node
                            for i in needed_neighbors:
                                message *= messages[(i, from_node)]

                            if from_node in evidence:
                                assert(evidence[from_node] in [0, 1])
                                zero_state = 0 if evidence[from_node] == 1 else 1
                                message[zero_state] = 0.0

                        # add message to dictionary
                        messages[(from_node, to_node)] = message
                        is_computed[from_node, to_node] = True
                    else:
                        # there is a message that we cannot compute yet. set all_computed=False
                        all_computed = False
        if all_computed:
            break

    # calculate marginals
    marginals = []
    for v in range(N/2):  # for each variable node
        m = 1.0
        # multiply the messages from all neighbors
        for f in get_neighbors(adj_fg, v):
            m *= messages[(f, v)]
        # normalize
        m /= np.sum(m)
        marginals.append(m)

    return marginals, messages


if __name__ == "__main__":
    """Wet grass example. Barber, Bayesian Reasoning, pg. 34.
        Variables:  Rain (R), Sprinkler (S), Jack's grass is wet (J), Tracey's grass is wet (T)
    """
    wg_adj = np.array([[0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.bool)
    wg_potentials = [np.array([0.8, 0.2]), np.array([0.9, 0.1]),
                     np.array([[0.8, 0.0], [0.2, 1.0]]),
                     np.array([[[1.0, 0.1], [0.0, 0.0]], [[0.0, 0.9], [1.0, 1.0]]])]
    wg_adj_fg, wg_factor_potentials = dag_to_fg(wg_adj, wg_potentials)
    wg_evidence = {3: 1}  # Tracey's grass is wet

    wg_probs, wg_messages = message_passing(wg_adj_fg, wg_factor_potentials, wg_evidence)

    # P(S=1|T=1) = 0.3382
    print wg_probs[1]

    wg_evidence = {2: 1, 3: 1}  # Jack's and Tracey's grass are wet
    wg_probs, wg_messages = message_passing(wg_adj_fg, wg_factor_potentials, wg_evidence)

    # P(S=1|T=1,J=1) = 0.1604
    print wg_probs[1]

    """
    my_adj = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]], dtype=np.bool)
    my_potentials = [np.array([0.3, 0.7]), np.array([0.4, 0.6]),
                     np.array([[0.6, 0.5], [0.4, 0.5]]),
                     np.array([[[0.1, 0.6], [0.5, 0.7]], [[0.9, 0.4], [0.5, 0.3]]])]
    my_adj_fg, my_factor_potentials = dag_to_fg(my_adj, my_potentials)

    my_marginals, my_messages = message_passing(my_adj_fg, my_factor_potentials)
    print my_marginals
    """


