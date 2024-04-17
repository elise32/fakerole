class FakeRoleStorageHelper:
    def __init__(self) -> None:
        pass

    def add_member(self, id:str, member: str) -> bool:
        return False

    def remove_member(self, id:str, member: str) -> bool:
        return False
    
    def delete_group(self, id:str) -> bool:
        return False
    
    def get_all(self) -> set[str, str, set[str]]:
        return None
