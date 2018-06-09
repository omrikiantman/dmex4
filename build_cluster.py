# TODO - add comments
from sklearn.cluster import KMeans


class BuildCluster:
    def __init__(self, n_clusters, n_init, df):
        self.n_clusters = n_clusters
        self.n_init = n_init
        self.df = df
        self.error_message = ""

    def build_cluster(self):
        # build a cluster using kmeans algo with random centroids
        # TODO - does random centroids means init = random?
        kmeans = KMeans(n_clusters=self.n_clusters, n_init=self.n_init, init='random')
        kmeans.fit(self.df.drop(['country'], axis=1))
        self.df['cluster'] = kmeans.labels_

    def verifications(self):
        # verify several tests to see if the file can be pre-processed
        funcs = [self.verify_n_clusters, self.verify_n_init]
        for f in funcs:
            self.error_message = f()
            if self.error_message != "":
                return False
        return True

    def verify_n_clusters(self):
        # verify it's an integer
        try:
            self.n_clusters = int(self.n_clusters)
            return "" if self.n_clusters > 0 else "n_clusters must be greater then 0"
        except ValueError:
            return "n_clusters must be an integer, not {}".format(self.n_clusters)

    def verify_n_init(self):
        # verify if the file can be pre-processed
        try:
            self.n_init = int(self.n_init)
            return "" if self.n_init > 0 else "n_init must be greater then 0"
        except ValueError:
            return "n_init must be an integer, not {}".format(self.n_init)
