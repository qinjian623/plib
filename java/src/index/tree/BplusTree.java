package index.tree;

import java.util.ArrayList;

public class BplusTree<Key extends Comparable<Key>, Value> {

	private int order;
	private Node root;

	// TODO may be we can alloc the memory at constructor.
	private class Node {

		private ArrayList<Pair<Key, Node>> leaves = new ArrayList<Pair<Key, Node>>();
		private Value val;

		public Node(Pair<Key, Value> p) {
			this.val = p.val;
		}

		public boolean isFull() {
			return this.leaves.size() >= order;
		}

		public boolean isLeaf() {
			return leaves.isEmpty();
		}

		public Node next(Pair<Key, Value> p) {
			for (int i = 0; i < leaves.size(); i++) {
				if (p.key.compareTo(leaves.get(i).key) < 0) {
					return leaves.get(i).val;
				}
			}
			return leaves.get(leaves.size() - 1).val;
		}
	}

	public BplusTree(int order) {
		this.order = order;
	}

	public BplusTree() {
		this.order = 3;
	}

	public void build(Iterable<Pair<Key, Value>> records) {
		for (Pair record : records) {

		}
	}

	public void insert(Pair<Key, Value> p) {
		Node node = this.search(root, p);
		if (node.isFull()) {

		} else {

		}
	}

	public void search(Pair<Key, Value> p) {
		Node node = search(root, p);
		p.val = node.val;
	}

	private Node search(Node node, Pair<Key, Value> p) {
		if (node.isLeaf()) {
			return node;
		}
		return search(node.next(p), p);
	}

	public void count() {

	}

}
