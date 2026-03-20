use std::collections::HashMap;

/// A simple key-value store with bounded capacity.
pub struct BoundedStore {
    data: HashMap<String, String>,
    capacity: usize,
}

impl BoundedStore {
    pub fn new(capacity: usize) -> Self {
        Self {
            data: HashMap::new(),
            capacity,
        }
    }

    pub fn get(&self, key: &str) -> Option<&String> {
        self.data.get(key)
    }

    pub fn insert(&mut self, key: String, value: String) -> Result<(), String> {
        if self.data.len() >= self.capacity && !self.data.contains_key(&key) {
            return Err(format!("Store is full (capacity: {})", self.capacity));
        }
        self.data.insert(key, value);
        Ok(())
    }

    pub fn remove(&mut self, key: &str) -> Option<String> {
        self.data.remove(key)
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }

    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    pub fn clear(&mut self) {
        self.data.clear();
    }

    pub fn contains_key(&self, key: &str) -> bool {
        self.data.contains_key(key)
    }

    pub fn keys(&self) -> Vec<&String> {
        self.data.keys().collect()
    }

    pub fn values(&self) -> Vec<&String> {
        self.data.values().collect()
    }

    pub fn iter(&self) -> impl Iterator<Item = (&String, &String)> {
        self.data.iter()
    }

    pub fn capacity(&self) -> usize {
        self.capacity
    }

    pub fn remaining(&self) -> usize {
        self.capacity.saturating_sub(self.data.len())
    }

    pub fn is_full(&self) -> bool {
        self.data.len() >= self.capacity
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_store_is_empty() {
        let store = BoundedStore::new(10);
        assert!(store.is_empty());
        assert_eq!(store.len(), 0);
        assert_eq!(store.capacity(), 10);
        assert_eq!(store.remaining(), 10);
        assert!(!store.is_full());
    }

    #[test]
    fn test_insert_and_get() {
        let mut store = BoundedStore::new(5);
        store.insert("key1".into(), "value1".into()).unwrap();
        assert_eq!(store.get("key1"), Some(&"value1".to_string()));
        assert_eq!(store.len(), 1);
        assert!(!store.is_empty());
    }

    #[test]
    fn test_insert_at_capacity_fails() {
        let mut store = BoundedStore::new(1);
        store.insert("key1".into(), "value1".into()).unwrap();
        let result = store.insert("key2".into(), "value2".into());
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("full"));
    }

    #[test]
    fn test_update_existing_key_at_capacity() {
        let mut store = BoundedStore::new(1);
        store.insert("key1".into(), "value1".into()).unwrap();
        store.insert("key1".into(), "updated".into()).unwrap();
        assert_eq!(store.get("key1"), Some(&"updated".to_string()));
        assert_eq!(store.len(), 1);
    }

    #[test]
    fn test_remove() {
        let mut store = BoundedStore::new(5);
        store.insert("key1".into(), "value1".into()).unwrap();
        let removed = store.remove("key1");
        assert_eq!(removed, Some("value1".to_string()));
        assert!(store.is_empty());
        assert_eq!(store.remove("nonexistent"), None);
    }

    #[test]
    fn test_clear() {
        let mut store = BoundedStore::new(5);
        store.insert("a".into(), "1".into()).unwrap();
        store.insert("b".into(), "2".into()).unwrap();
        store.clear();
        assert!(store.is_empty());
        assert_eq!(store.remaining(), 5);
    }

    #[test]
    fn test_contains_key() {
        let mut store = BoundedStore::new(5);
        store.insert("key1".into(), "value1".into()).unwrap();
        assert!(store.contains_key("key1"));
        assert!(!store.contains_key("key2"));
    }

    #[test]
    fn test_keys_and_values() {
        let mut store = BoundedStore::new(5);
        store.insert("a".into(), "1".into()).unwrap();
        store.insert("b".into(), "2".into()).unwrap();
        assert_eq!(store.keys().len(), 2);
        assert_eq!(store.values().len(), 2);
    }

    #[test]
    fn test_iter() {
        let mut store = BoundedStore::new(5);
        store.insert("a".into(), "1".into()).unwrap();
        store.insert("b".into(), "2".into()).unwrap();
        let items: Vec<_> = store.iter().collect();
        assert_eq!(items.len(), 2);
    }

    #[test]
    fn test_remaining_and_full() {
        let mut store = BoundedStore::new(2);
        assert_eq!(store.remaining(), 2);
        assert!(!store.is_full());
        store.insert("a".into(), "1".into()).unwrap();
        assert_eq!(store.remaining(), 1);
        store.insert("b".into(), "2".into()).unwrap();
        assert_eq!(store.remaining(), 0);
        assert!(store.is_full());
    }
}
