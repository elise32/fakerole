import re

from FakeRoleStorageHelper import FakeRoleStorageHelper

class NameSizeError(Exception):
    pass

class MemberSizeError(Exception):
    pass

class IDSizeError(Exception):
    pass

def __is_valid_members_set(self, members: set[str]) -> bool:
    return (
        members
        and len(members) <= FakeRole.MEMBERS_MAX_SIZE
        and all(is_valid_member(member) for member in members)
    )
    
def is_valid_member(self, member:str) -> bool:
    """
    Checks if member is a valid Discord snowflake
    """
    return bool(re.match(r'^[0-9]{17,20}$', member))

class FakeRole:
    NAME_MAX_LENGTH = 30
    MEMBERS_MAX_SIZE = 40

    def __init__(self, id: str, name: str, members: set[str]):
        if not id:
            raise IDSizeError("ID for FakeRole cannot be none")
        self._id: str = id

        self.name: str = name

        if not __is_valid_members_set(members):
            raise MemberSizeError(f"Member size for FakeRole {self.id} {self.name} was incorrect, \
                                  was {len(members)}")
        self._members: set[str] = members
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name:str) -> str:
        if not name or len(name) > self.NAME_MAX_LENGTH:
            raise NameSizeError(f"Name for FakeRole {self.id} {self.name} was incorrect, tried to \
                                set it to {name}, must be <= {self.NAME_MAX_LENGTH}")
        self._name = name

    @property
    def members(self) -> frozenset:
        """
        Do not directly modify members. Instead use FakeRole.add and FakeRole.remove
        """
        return self._members
    
    def add(self, member) -> bool:
        """
        Adds member to fake role and updates the storage.
        Returns whether or not the member was successfully added.
        """
        # Sanity check
        if len(self.members) > FakeRole.MEMBERS_MAX_SIZE:
            raise MemberSizeError("Somehow, the FakeRole was above capacity")
        if len(self.members) == FakeRole.MEMBERS_MAX_SIZE:
            return False
        if not is_valid_member(member):
            return False
        
        self._members.add(member)
        storage_helper.add_member(self.id, member)
        return True
    
    def remove(self, member) -> bool:
        """
        Removes member to fake role and updates the storage. Deletes the group from storage if group
        become empty
        Returns whether the member was successfully removed. 
        """
        if not is_valid_member(member):
            return False
        
        self._members.remove(member)
        FakeRoleStorageHelper.remove_member(self.id, member)
        if not self.members:
            storage_helper.delete_group(self.id)
        return True

def get_all_FakeRoles() -> set[FakeRole]:
    return storage_helper.get_all()

storage_helper = FakeRoleStorageHelper()